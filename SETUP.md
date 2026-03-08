# Dharti Drishti - Setup Guide

## Installation

1. Install dependencies:
```bash
uv sync
```

Or if using pip:
```bash
pip install flask flask-cors
```

## Running the Application

### Start Backend Server
```bash
python backend/app.py
```
The backend will run on `http://localhost:5000`

### Open Frontend
Open `frontend/index.html` in your browser, or serve it with:
```bash
cd frontend
python -m http.server 8000
```
Then visit `http://localhost:8000`

## Usage

1. Allow browser location access when prompted
2. Upload a soil image
3. Set number of top crops (default: 2)
4. Click "Analyze Soil"
5. View the JSON results

## API Endpoints

- `POST /api/analyze` - Analyze soil image
  - Form data: `image`, `latitude`, `longitude`, `top_best_crop`
- `GET /api/health` - Health check
