#!/bin/bash

# EC2 Deployment Script
# Run this script ON YOUR EC2 INSTANCE after uploading files

echo "🚀 Dharti Drishti - EC2 Deployment Script"
echo "=========================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create .env file with your environment variables"
    echo "Run: nano .env"
    exit 1
fi

echo "✅ .env file found"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed!"
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker ubuntu
    echo "✅ Docker installed. Please logout and login again, then run this script again."
    exit 0
fi

echo "✅ Docker is installed"
echo ""

# Stop and remove old container if exists
if [ "$(docker ps -aq -f name=dharti-drishti-app)" ]; then
    echo "🛑 Stopping old container..."
    docker stop dharti-drishti-app
    docker rm dharti-drishti-app
    echo "✅ Old container removed"
    echo ""
fi

# Build Docker image
echo "🔨 Building Docker image..."
docker build -t dharti-drishti:latest .

if [ $? -ne 0 ]; then
    echo "❌ Docker build failed!"
    exit 1
fi

echo "✅ Docker image built successfully"
echo ""

# Run container
echo "🚀 Starting container..."
docker run -d \
  --name dharti-drishti-app \
  -p 80:5000 \
  --env-file .env \
  --restart unless-stopped \
  dharti-drishti:latest

if [ $? -ne 0 ]; then
    echo "❌ Failed to start container!"
    exit 1
fi

echo "✅ Container started successfully"
echo ""

# Wait a few seconds for container to start
echo "⏳ Waiting for application to start..."
sleep 5

# Check if container is running
if [ "$(docker ps -q -f name=dharti-drishti-app)" ]; then
    echo "✅ Container is running!"
    echo ""
    
    # Get EC2 public IP
    PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
    
    echo "=========================================="
    echo "🎉 Deployment Successful!"
    echo "=========================================="
    echo ""
    echo "Your application is now live at:"
    echo "🌐 Frontend: http://$PUBLIC_IP/"
    echo "🔌 API Health: http://$PUBLIC_IP/api/health"
    echo ""
    echo "To view logs:"
    echo "  docker logs -f dharti-drishti-app"
    echo ""
    echo "To restart:"
    echo "  docker restart dharti-drishti-app"
    echo ""
    echo "To stop:"
    echo "  docker stop dharti-drishti-app"
    echo ""
else
    echo "❌ Container failed to start!"
    echo "Checking logs..."
    docker logs dharti-drishti-app
    exit 1
fi
