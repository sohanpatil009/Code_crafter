#!/bin/bash

# Script to download New Plant Diseases Dataset from Kaggle

echo "📥 Downloading New Plant Diseases Dataset from Kaggle"
echo "======================================================"
echo ""

# Check if kaggle is installed
if ! command -v kaggle &> /dev/null; then
    echo "❌ Kaggle CLI not found!"
    echo "📦 Installing kaggle..."
    pip install kaggle
fi

# Check if kaggle.json exists
if [ ! -f ~/.kaggle/kaggle.json ]; then
    echo "❌ Kaggle API token not found!"
    echo ""
    echo "📝 Please follow these steps:"
    echo "1. Go to https://www.kaggle.com/settings"
    echo "2. Click 'Create New API Token'"
    echo "3. Download kaggle.json"
    echo "4. Move it to ~/.kaggle/kaggle.json"
    echo "5. Run: chmod 600 ~/.kaggle/kaggle.json"
    echo ""
    exit 1
fi

# Create data directory
echo "📁 Creating data directory..."
mkdir -p data

# Download dataset
echo "📥 Downloading dataset (this may take 5-15 minutes)..."
kaggle datasets download -d vipoooool/new-plant-diseases-dataset

# Check if download was successful
if [ ! -f "new-plant-diseases-dataset.zip" ]; then
    echo "❌ Download failed!"
    exit 1
fi

echo "✅ Download complete!"
echo ""

# Get file size
SIZE=$(du -h new-plant-diseases-dataset.zip | cut -f1)
echo "📦 Downloaded file size: $SIZE"
echo ""

# Extract dataset
echo "📂 Extracting dataset..."
unzip -q new-plant-diseases-dataset.zip -d data/

# Check extraction
if [ $? -eq 0 ]; then
    echo "✅ Extraction complete!"
else
    echo "❌ Extraction failed!"
    exit 1
fi

# Remove zip file
echo "🗑️  Removing zip file..."
rm new-plant-diseases-dataset.zip

# Count classes
echo ""
echo "📊 Dataset Statistics:"
if [ -d "data/train" ]; then
    TRAIN_CLASSES=$(ls data/train | wc -l)
    echo "   Training classes: $TRAIN_CLASSES"
fi

if [ -d "data/valid" ]; then
    VALID_CLASSES=$(ls data/valid | wc -l)
    echo "   Validation classes: $VALID_CLASSES"
fi

# Show directory structure
echo ""
echo "📁 Directory structure:"
tree -L 2 data/ 2>/dev/null || ls -R data/ | head -50

echo ""
echo "======================================================"
echo "✅ Dataset setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Verify dataset: ls data/train/ | wc -l (should show 38)"
echo "2. Seed database: python seed_data.py"
echo "3. Train model: python models/train.py"
echo ""
