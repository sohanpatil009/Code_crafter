#!/bin/bash

echo "🚀 Crop Disease Detection Backend - Quick Start"
echo "=============================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file from example..."
    cp .env.example .env
    echo "⚠️ Please edit .env file with your configuration"
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p uploads
mkdir -p audio_files/generated

# Run the application
echo ""
echo "✅ Setup complete!"
echo "🚀 Starting Flask server..."
echo ""
python app.py
