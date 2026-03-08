// Automatically detect API URL based on environment
const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:5000/api'
    : `${window.location.origin}/api`;
const DEMO_LOCATION = { lat: 23.1456, lon: 72.5325 };

window.addEventListener('DOMContentLoaded', () => {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                document.getElementById('latitude').value = lat;
                document.getElementById('longitude').value = lon;
                document.getElementById('locationText').textContent = `${lat.toFixed(4)}, ${lon.toFixed(4)}`;
            },
            (error) => {
                document.getElementById('locationText').textContent = 'Unable to detect location';
                console.error('Location error:', error);
            }
        );
    } else {
        document.getElementById('locationText').textContent = 'Geolocation not supported';
    }
    
    // Demo mode toggle
    document.getElementById('demoMode').addEventListener('change', (e) => {
        const isDemoMode = e.target.checked;
        document.getElementById('demoImageSelector').style.display = isDemoMode ? 'block' : 'none';
        document.getElementById('uploadImageSection').style.display = isDemoMode ? 'none' : 'block';
        document.getElementById('imageInput').required = !isDemoMode;
        
        if (isDemoMode) {
            // Set demo location
            document.getElementById('latitude').value = DEMO_LOCATION.lat;
            document.getElementById('longitude').value = DEMO_LOCATION.lon;
            document.getElementById('locationText').textContent = `${DEMO_LOCATION.lat}, ${DEMO_LOCATION.lon} (Demo Location)`;
            
            // Show preview of selected demo image
            updateDemoImagePreview();
        } else {
            // Restore actual location if available
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        const lat = position.coords.latitude;
                        const lon = position.coords.longitude;
                        document.getElementById('latitude').value = lat;
                        document.getElementById('longitude').value = lon;
                        document.getElementById('locationText').textContent = `${lat.toFixed(4)}, ${lon.toFixed(4)}`;
                    }
                );
            }
        }
    });
    
    // Demo image selection change
    document.getElementById('demoImageSelect').addEventListener('change', updateDemoImagePreview);
});

function updateDemoImagePreview() {
    const selectedImage = document.getElementById('demoImageSelect').value;
    const preview = document.getElementById('demoImagePreview');
    preview.innerHTML = `<img src="${API_URL.replace('/api', '')}/storage_service/soil_images/${selectedImage}" alt="Demo soil preview">`;
}

document.getElementById('imageInput').addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (event) => {
            const preview = document.getElementById('imagePreview');
            preview.innerHTML = `<img src="${event.target.result}" alt="Soil preview">`;
        };
        reader.readAsDataURL(file);
    }
});

document.getElementById('analysisForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const isDemoMode = document.getElementById('demoMode').checked;
    const latitude = document.getElementById('latitude').value;
    const longitude = document.getElementById('longitude').value;
    const topCrops = document.getElementById('topCrops').value;
    
    if (!latitude || !longitude) {
        showError('Location not detected. Please enable location services.');
        return;
    }
    
    // Validate image selection
    if (!isDemoMode) {
        const imageFile = document.getElementById('imageInput').files[0];
        if (!imageFile) {
            showError('Please upload an image or use demo mode.');
            return;
        }
    }
    
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('success').classList.add('hidden');
    document.getElementById('error').classList.add('hidden');
    document.getElementById('submitBtn').disabled = true;
    
    const formData = new FormData();
    
    if (isDemoMode) {
        const demoImage = document.getElementById('demoImageSelect').value;
        formData.append('demo_image', demoImage);
    } else {
        const imageFile = document.getElementById('imageInput').files[0];
        formData.append('image', imageFile);
    }
    
    formData.append('latitude', latitude);
    formData.append('longitude', longitude);
    formData.append('top_best_crop', topCrops);
    
    try {
        const response = await fetch(`${API_URL}/analyze`, { method: 'POST', body: formData });
        const data = await response.json();
        if (data.success) {
            showResults(data.data);
        } else {
            showError(data.error || 'Analysis failed');
        }
    } catch (error) {
        showError(`Error: ${error.message}`);
    } finally {
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('submitBtn').disabled = false;
    }
});

function showResults(data) {
    console.log('Received data:', data);
    sessionStorage.setItem('analysisResults', JSON.stringify(data));
    const successDiv = document.getElementById('success');
    successDiv.classList.remove('hidden');
    document.getElementById('viewResultsBtn').addEventListener('click', () => {
        window.location.href = 'results.html';
    });
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}
