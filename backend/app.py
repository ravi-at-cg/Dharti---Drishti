import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Add parent directory to path to import ai_services
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_services.ai_layer_service import process_image

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'storage_service/soil_images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/analyze', methods=['POST'])
def analyze_soil():
    try:
        # Get parameters
        latitude = float(request.form.get('latitude'))
        longitude = float(request.form.get('longitude'))
        top_best_crop = int(request.form.get('top_best_crop', 2))
        
        # Check if using demo image or uploaded image
        if 'demo_image' in request.form:
            # Use demo image
            demo_image_name = request.form.get('demo_image')
            image_path = os.path.join(UPLOAD_FOLDER, demo_image_name)
            
            if not os.path.exists(image_path):
                return jsonify({'error': f'Demo image {demo_image_name} not found'}), 400
        else:
            # Check if image file is present
            if 'image' not in request.files:
                return jsonify({'error': 'No image file provided'}), 400
            
            file = request.files['image']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            # Save uploaded image
            filename = secure_filename(file.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(image_path)
        
        # Process image
        result = process_image(image_path, latitude, longitude, top_best_crop)
        
        # Parse the JSON string returned by the AI
        import json
        try:
            parsed_result = json.loads(result)
        except json.JSONDecodeError:
            # If parsing fails, return the raw result
            parsed_result = {"raw_output": result}
        
        return jsonify({
            'success': True,
            'data': parsed_result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})

@app.route('/storage_service/soil_images/<filename>')
def serve_demo_image(filename):
    """Serve demo images for preview"""
    from flask import send_from_directory
    # Get the absolute path to the storage directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    images_dir = os.path.join(base_dir, 'storage_service', 'soil_images')
    return send_from_directory(images_dir, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
