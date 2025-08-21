#!/bin/bash

# Railway deployment script for Binary Piper TTS
echo "🚀 Starting Binary Piper TTS deployment..."

# Install system dependencies
echo "📦 Installing system dependencies..."
apt-get update
apt-get install -y wget curl python3-pip espeak-ng espeak-ng-data

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install -r requirements.txt

# Download Piper binary
echo "⬇️ Downloading Piper binary..."
wget -O piper.tar.gz "https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz"
tar -xzf piper.tar.gz
mv piper/piper /usr/local/bin/
chmod +x /usr/local/bin/piper
rm -rf piper.tar.gz piper/

# Create models directory
mkdir -p models

# Download voice models
echo "🗣️ Downloading voice models..."
python3 download_models.py

echo "✅ Deployment complete! Starting service..."

# Start the service
python3 app.py
