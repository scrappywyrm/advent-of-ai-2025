#!/bin/bash

# Deploy static website from Day02 to Vercel Production
# Winter Festival Launch Script

echo "🌨️  Winter Festival Site Deployment Starting..."

# Navigate to Day02 directory
cd ../Day02

echo "📁 Current directory: $(pwd)"
echo "📋 Checking source files..."

# Check if operator_story.html exists
if [ -f "operator_story.html" ]; then
    echo "✅ Found operator_story.html"
    
    # Copy operator_story.html to index.html for automatic loading
    echo "📄 Copying operator_story.html to index.html..."
    cp operator_story.html index.html
    echo "✅ index.html created successfully"
else
    echo "❌ Error: operator_story.html not found in source directory"
    exit 1
fi

echo "🚀 Deploying to Vercel Production..."

# Deploy using Vercel CLI with exact specifications
vercel --prod --yes --name day04

# Capture deployment status
DEPLOY_STATUS=$?

if [ $DEPLOY_STATUS -eq 0 ]; then
    echo "🎉 Deployment successful!"
    
    # Echo the final Vercel URL
    echo "🌐 Site deployed to: https://day04.vercel.app"
    echo "✨ Winter Festival site is now live!"
else
    echo "❌ Deployment failed with status code: $DEPLOY_STATUS"
    exit 1
fi
