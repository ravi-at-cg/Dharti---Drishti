# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies for OpenCV and other libraries
RUN apt-get update && apt-get install -y \
    gcc \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgthread-2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml ./

# Install uv for faster dependency installation
RUN pip install --no-cache-dir uv

# Install Python dependencies
RUN uv pip install --system --no-cache \
    boto3>=1.42.63 \
    dotenv>=0.9.9 \
    google-genai>=1.66.0 \
    groq>=1.0.0 \
    inference-sdk>=1.1.0 \
    roboflow>=1.2.16 \
    sarvamai>=0.1.26 \
    flask>=3.0.0 \
    flask-cors>=4.0.0 \
    gunicorn>=21.2.0

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p storage_service/soil_images storage_service/model_outputs

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=backend/app.py
ENV PYTHONUNBUFFERED=1

# Run with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "backend.app:app"]
