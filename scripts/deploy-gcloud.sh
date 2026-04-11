#!/bin/bash
# Deploy to Google Cloud Run (free tier available)

APP_NAME="heart-risk-app"
REGION="us-central1"

echo "🌐 Deploying to Google Cloud Run..."
echo "Make sure you've run: gcloud auth login"
echo ""

gcloud run deploy $APP_NAME \
    --source . \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 1Gi \
    --timeout 3600

echo ""
echo "✅ Deployment complete!"
echo "Your app URL will be displayed above"
