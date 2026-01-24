# 📊 Dataset Setup Guide

## Dataset Information

We're using the **New Plant Diseases Dataset** from Kaggle, which is one of the most comprehensive plant disease datasets available.

### Dataset Details
- **Source**: Kaggle - [New Plant Diseases Dataset](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset)
- **Total Images**: ~87,000 RGB images
- **Classes**: 38 different classes (diseases + healthy plants)
- **Image Format**: JPG/JPEG
- **Split**: 80% training, 20% validation
- **Quality**: High-quality, labeled images

### Crops Covered
1. **Apple** - 4 classes (3 diseases + healthy)
2. **Tomato** - 10 classes (9 diseases + healthy)
3. **Potato** - 3 classes (2 diseases + healthy)
4. **Corn (Maize)** - 4 classes (3 diseases + healthy)
5. **Grape** - 4 classes (3 diseases + healthy)
6. **Pepper (Bell)** - 2 classes (1 disease + healthy)
7. **Cherry** - 2 classes (1 disease + healthy)
8. **Peach** - 2 classes (1 disease + healthy)
9. **Strawberry** - 2 classes (1 disease + healthy)
10. **Blueberry** - 1 class (healthy)
11. **Raspberry** - 1 class (healthy)
12. **Soybean** - 1 class (healthy)
13. **Squash** - 1 class (powdery mildew)
14. **Orange** - 1 class (haunglongbing)

---

## 🚀 Quick Setup

### Step 1: Download Dataset from Kaggle

#### Option A: Using Kaggle API (Recommended)

1. **Install Kaggle CLI**
```bash
pip install kaggle
```

2. **Setup Kaggle API Token**
   - Go to https://www.kaggle.com/settings
   - Click "Create New API Token"
   - Download `kaggle.json`
   - Place it in `~/.kaggle/kaggle.json`
   - Set permissions: `chmod 600 ~/.kaggle/kaggle.json`

3. **Download Dataset**
```bash
cd backend
kaggle datasets download -d vipoooool/new-plant-diseases-dataset
unzip new-plant-diseases-dataset.zip -d data/
rm new-plant-diseases-dataset.zip
```

#### Option B: Manual Download

1. Visit: https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset
2. Click "Download" button
3. Extract to `backend/data/` folder

---

### Step 2: Organize Dataset

After download, your structure should be:

```
backend/
├── data/
│   ├── train/
│   │   ├── Apple___Apple_scab/
│   │   ├── Apple___Black_rot/
│   │   ├── Apple___Cedar_apple_rust/
│   │   ├── Apple___healthy/
│   │   ├── Tomato___Bacterial_spot/
│   │   ├── Tomato___Early_blight/
│   │   ├── Tomato___Late_blight/
│   │   ├── Tomato___healthy/
│   │   ├── Potato___Early_blight/
│   │   ├── Potato___Late_blight/
│   │   ├── Potato___healthy/
│   │   ├── Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot/
│   │   ├── Corn_(maize)___Common_rust_/
│   │   ├── Corn_(maize)___Northern_Leaf_Blight/
│   │   ├── Corn_(maize)___healthy/
│   │   └── ... (38 classes total)
│   │
│   ├── valid/
│   │   └── ... (same structure as train)
│   │
│   └── test/
│       └── ... (test images)
```

---

## 📋 Complete Class List (38 Classes)

### Apple (4 classes)
1. Apple___Apple_scab
2. Apple___Black_rot
3. Apple___Cedar_apple_rust
4. Apple___healthy

### Blueberry (1 class)
5. Blueberry___healthy

### Cherry (2 classes)
6. Cherry_(including_sour)___Powdery_mildew
7. Cherry_(including_sour)___healthy

### Corn (Maize) (4 classes)
8. Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot
9. Corn_(maize)___Common_rust_
10. Corn_(maize)___Northern_Leaf_Blight
11. Corn_(maize)___healthy

### Grape (4 classes)
12. Grape___Black_rot
13. Grape___Esca_(Black_Measles)
14. Grape___Leaf_blight_(Isariopsis_Leaf_Spot)
15. Grape___healthy

### Orange (1 class)
16. Orange___Haunglongbing_(Citrus_greening)

### Peach (2 classes)
17. Peach___Bacterial_spot
18. Peach___healthy

### Pepper (Bell) (2 classes)
19. Pepper,_bell___Bacterial_spot
20. Pepper,_bell___healthy

### Potato (3 classes)
21. Potato___Early_blight
22. Potato___Late_blight
23. Potato___healthy

### Raspberry (1 class)
24. Raspberry___healthy

### Soybean (1 class)
25. Soybean___healthy

### Squash (1 class)
26. Squash___Powdery_mildew

### Strawberry (2 classes)
27. Strawberry___Leaf_scorch
28. Strawberry___healthy

### Tomato (10 classes)
29. Tomato___Bacterial_spot
30. Tomato___Early_blight
31. Tomato___Late_blight
32. Tomato___Leaf_Mold
33. Tomato___Septoria_leaf_spot
34. Tomato___Spider_mites Two-spotted_spider_mite
35. Tomato___Target_Spot
36. Tomato___Tomato_Yellow_Leaf_Curl_Virus
37. Tomato___Tomato_mosaic_virus
38. Tomato___healthy

---

## 🔧 Update Backend Configuration

The backend has been updated to support all 38 classes. Check these files:

1. **config.py** - Updated with all disease classes
2. **seed_data.py** - Updated with comprehensive disease information
3. **ml_service.py** - Ready to load model trained on this dataset

---

## 🤖 Training ML Model

### Using the Dataset

```python
# Example training script
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Data augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

valid_datagen = ImageDataGenerator(rescale=1./255)

# Load data
train_generator = train_datagen.flow_from_directory(
    'data/train',
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

valid_generator = valid_datagen.flow_from_directory(
    'data/valid',
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

# Train model (see models/train.py for complete implementation)
```

---

## 📊 Dataset Statistics

- **Training Images**: ~70,000 images
- **Validation Images**: ~17,000 images
- **Image Size**: Variable (will be resized to 224x224)
- **Color Space**: RGB
- **File Format**: JPG/JPEG
- **Classes**: 38 (balanced distribution)

---

## 🎯 Why This Dataset?

### Advantages:
1. ✅ **Large Scale**: 87K+ images for robust training
2. ✅ **Diverse**: 14 different crops covered
3. ✅ **Real-world**: High-quality, real disease images
4. ✅ **Well-organized**: Pre-split into train/valid/test
5. ✅ **Popular**: Widely used in research (proven results)
6. ✅ **Maintained**: Active Kaggle dataset with community support

### Comparison with Google Drive Dataset:
- Kaggle dataset is more comprehensive (38 vs fewer classes)
- Better organized and documented
- Larger dataset size
- Community-tested and validated
- Easier to download and setup

---

## 🚀 Next Steps

1. **Download Dataset**
   ```bash
   cd backend
   kaggle datasets download -d vipoooool/new-plant-diseases-dataset
   unzip new-plant-diseases-dataset.zip -d data/
   ```

2. **Verify Structure**
   ```bash
   ls data/train/ | wc -l  # Should show 38
   ```

3. **Update Disease Database**
   ```bash
   python seed_data.py
   ```

4. **Train Model** (Prathamesh's task)
   ```bash
   python models/train.py
   ```

5. **Test Backend**
   ```bash
   python app.py
   ./test_api.sh
   ```

---

## 📝 Notes

- Dataset size: ~3.5 GB (compressed), ~4.5 GB (extracted)
- Download time: 5-15 minutes (depending on internet speed)
- Training time: 2-4 hours on GPU, 12-24 hours on CPU
- Model size: ~100-200 MB (after training)

---

## 🐛 Troubleshooting

### Issue: Kaggle API not working
```bash
# Check if kaggle.json exists
ls ~/.kaggle/

# Set correct permissions
chmod 600 ~/.kaggle/kaggle.json
```

### Issue: Unzip error
```bash
# Install unzip
sudo apt-get install unzip

# Or use Python
python -m zipfile -e new-plant-diseases-dataset.zip data/
```

### Issue: Not enough disk space
- Dataset needs ~5 GB free space
- Clear cache: `rm -rf ~/.cache/`
- Use external drive if needed

---

## 📚 References

- [Kaggle Dataset](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset)
- [PlantVillage Project](https://plantvillage.psu.edu/)
- [Research Paper](https://arxiv.org/abs/1511.08060)

---

**Happy Training! 🌱🤖**
