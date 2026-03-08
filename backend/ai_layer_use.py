from fastapi import FastAPI, HTTPException
from PIL import Image
import json
import os

app = FastAPI()

def process_image_to_json(image_path: str) -> dict:
    """
    Process an image and return metadata as JSON
    """
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        with Image.open(image_path) as img:
            return {
                "filename": os.path.basename(image_path),
                "format": img.format,
                "mode": img.mode,
                "size": {
                    "width": img.size[0],
                    "height": img.size[1]
                },
                "has_transparency": img.mode in ("RGBA", "LA") or "transparency" in img.info
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")

@app.get("/image-info/{image_path:path}")
async def get_image_info(image_path: str):
    """
    Get image information as JSON
    """
    return process_image_to_json(image_path)

# Sample usage
if __name__ == "__main__":
    import uvicorn
    
    # Example usage of the function
    sample_path = "sample.jpg"  # Replace with actual image path
    try:
        result = process_image_to_json(sample_path)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")
    
    # Run the FastAPI server
    uvicorn.run(app, host="0.0.0.0", port=8000)
