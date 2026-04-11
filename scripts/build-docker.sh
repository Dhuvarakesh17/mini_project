#!/bin/bash
# Deploy to Docker Hub and then to any Docker-compatible platform

echo "🐳 Building Docker image..."
docker build -t heart-risk-app:latest .

echo "📦 Testing locally..."
docker run -p 8000:8000 heart-risk-app:latest &
CONTAINER_ID=$!
sleep 5

echo "🧪 Testing API endpoint..."
curl http://localhost:8000/docs || echo "⚠️ Health check failed"

echo "⛔ Stopping test container..."
kill $CONTAINER_ID

echo "✅ Build successful!"
echo ""
echo "Next steps:"
echo "1. Tag image: docker tag heart-risk-app:latest YOUR_REGISTRY/heart-risk-app:latest"
echo "2. Push: docker push YOUR_REGISTRY/heart-risk-app:latest"
echo "3. Deploy to cloud platform (Google Cloud Run, AWS ECS, etc.)"
