#!/bin/bash

# Stop and remove the old container
echo "Stopping old container..."
docker stop dharti-drishti-app
docker rm dharti-drishti-app

# Rebuild the image with fixes
echo "Rebuilding Docker image..."
docker build -t dharti-drishti:latest .

# Run the new container
echo "Starting new container..."
docker run -d --name dharti-drishti-app -p 5000:5000 --env-file .env dharti-drishti:latest

# Wait a few seconds for startup
echo "Waiting for container to start..."
sleep 5

# Show logs
echo "Container logs:"
docker logs dharti-drishti-app

echo ""
echo "Container status:"
docker ps | grep dharti-drishti-app
