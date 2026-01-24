# Backend Implementation Guide
## For Pratham (Backend) & Prathamesh (ML)

---

## 🎯 Goal
Connect the Android app to live backend API for real-time crop disease detection.

---

## 📱 Current Status

### ✅ Mobile App (Sohan) - COMPLETE
- Native Android app with CameraX
- Image capture and upload functionality
- API client with Retrofit
- Results display with 8 languages
- Audio playback support
- **Currently using mock data (backend not available)**

### ⏳ Backend (Pratham) - PENDING
- Flask/FastAPI server setup needed
- API endpoints implementation required
- ML model integration needed
- TTS service implementation needed

### ⏳ ML Model (Prathamesh) - PENDING
- Trained model integration
- Image preprocessing pipeline
- Disease prediction logic

---

## 🔌 API Endpoints Required

The Android app is expecting these endpoints:

### 1. Disease Prediction Endpoint
```
POST /api/predict
```

**Request:**
- Content-Type: `multipart/form-data`
- Parameters:
  - `image`: Image file (JPEG, 80% compressed)
  - `language`: Language code (en, hi, mr, ta, te, gu, pa, bn)

**Expected Response:**
```json
{
  "disease_name": "Tomato Early Blight",
  "confidence": 0.95,
  "description": "Early blight is a common fungal disease affecting tomato plants...",
  "treatment": "Remove infected leaves, apply copper-based fungicide...",
  "audio_url": "http://localhost:5000/audio/generated/disease_123.mp3",
  "language": "en"
}
```

**Response Fields:**
- `disease_name` (string): Name of detected disease
- `confidence` (float): Confidence score between 0 and 1
- `description` (string): Disease description in selected language
- `treatment` (string): Treatment recommendations in selected language
- `audio_url` (string, optional): URL to audio file
- `language` (string): Language code used

---

### 2. Text-to-Speech Endpoint
```
POST /api/tts/generate
```

**Request:**
- Content-Type: `application/json` or Query Parameters
- Parameters:
  - `text`: Text to convert to speech
  - `language`: Language code (en, hi, mr, ta, te, gu, pa, bn)

**Expected Response:**
```json
{
  "audio_url": "http://localhost:5000/audio/generated/tts_456.mp3",
  "audio_id": "tts_456",
  "success": true,
  "message": "Audio generated successfully"
}
```

---

### 3. Supported Languages Endpoint
```
GET /api/languages
```

**Expected Response:**
```json
{
  "languages": [
    {
      "code": "en",
      "name": "English",
      "native_name": "English"
    },
    {
      "code": "hi",
      "name": "Hindi",
      "native_name": "हिंदी"
    },
    {
      "code": "mr",
      "name": "Marathi",
      "native_name": "मराठी"
    },
    {
      "code": "ta",
      "name": "Tamil",
      "native_name": "தமிழ்"
    },
    {
      "code": "te",
      "name": "Telugu",
      "native_name": "తెలుగు"
    },
    {
      "code": "gu",
      "name": "Gujarati",
      "native_name": "ગુજરાતી"
    },
    {
      "code": "pa",
      "name": "Punjabi",
      "native_name": "ਪੰਜਾਬੀ"
    },
    {
      "code": "bn",
      "name": "Bengali",
      "native_name": "বাংলা"
    }
  ]
}
```

---

## 🛠️ Implementation Steps

### For Pratham (Backend Developer)

#### Step 1: Setup Flask/FastAPI Project

**Option A: Flask**
```bash
# Create project structure
mkdir backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install flask flask-cors pillow gtts googletrans==4.0.0rc1
pip install tensorflow keras numpy opencv-python

# Create requirements.txt
pip freeze > requirements.txt
```

**Option B: FastAPI**
```bash
pip install fastapi uvicorn python-multipart pillow gtts googletrans==4.0.0rc1
pip install tensorflow keras numpy opencv-python
```

---

#### Step 2: Create Flask App Structure

```
backend/
├── app.py                      # Main Flask application
├── api/
│   ├── __init__.py
│   ├── routes.py              # API endpoints
│   └── validators.py          # Request validation
├── services/
│   ├── __init__.py
│   ├── ml_service.py          # ML model inference (Prathamesh)
│   ├── tts_service.py         # Text-to-speech
│   └── translation_service.py # Translation
├── models/
│   └── crop_disease_model.h5  # Trained model (Prathamesh)
├── audio_files/
│   └── generated/             # Generated audio files
├── config.py                  # Configuration
└── requirements.txt
```

---

#### Step 3: Implement app.py

```python
# backend/app.py
from flask import Flask
from flask_cors import CORS
from api.routes import api_bp
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for Android app

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['AUDIO_FOLDER'] = 'audio_files/generated'

# Create folders if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)

# Register blueprints
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def home():
    return {
        "message": "Crop Disease Detection API",
        "status": "running",
        "version": "1.0"
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

---

#### Step 4: Implement API Routes

```python
# backend/api/routes.py
from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from services.ml_service import predict_disease
from services.tts_service import generate_audio
from services.translation_service import translate_text
import os

api_bp = Blueprint('api', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api_bp.route('/predict', methods=['POST'])
def predict():
    """Disease prediction endpoint"""
    try:
        # Check if image is in request
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        language = request.form.get('language', 'en')
        
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file and allowed_file(file.filename):
            # Save uploaded file
            filename = secure_filename(file.filename)
            filepath = os.path.join('uploads', filename)
            file.save(filepath)
            
            # Get prediction from ML service (Prathamesh's code)
            result = predict_disease(filepath, language)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify(result), 200
        else:
            return jsonify({'error': 'Invalid file type'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tts/generate', methods=['POST'])
def generate_tts():
    """Text-to-speech generation endpoint"""
    try:
        data = request.get_json() if request.is_json else request.args
        text = data.get('text')
        language = data.get('language', 'en')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Generate audio
        audio_result = generate_audio(text, language)
        
        return jsonify(audio_result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/languages', methods=['GET'])
def get_languages():
    """Get supported languages"""
    languages = [
        {"code": "en", "name": "English", "native_name": "English"},
        {"code": "hi", "name": "Hindi", "native_name": "हिंदी"},
        {"code": "mr", "name": "Marathi", "native_name": "मराठी"},
        {"code": "ta", "name": "Tamil", "native_name": "தமிழ்"},
        {"code": "te", "name": "Telugu", "native_name": "తెలుగు"},
        {"code": "gu", "name": "Gujarati", "native_name": "ગુજરાતી"},
        {"code": "pa", "name": "Punjabi", "native_name": "ਪੰਜਾਬੀ"},
        {"code": "bn", "name": "Bengali", "native_name": "বাংলা"}
    ]
    return jsonify({"languages": languages}), 200

@api_bp.route('/audio/<path:filename>', methods=['GET'])
def serve_audio(filename):
    """Serve audio files"""
    try:
        audio_path = os.path.join('audio_files/generated', filename)
        return send_file(audio_path, mimetype='audio/mpeg')
    except Exception as e:
        return jsonify({'error': str(e)}), 404
```

---

#### Step 5: Implement TTS Service

```python
# backend/services/tts_service.py
from gtts import gTTS
import os
import uuid

def generate_audio(text, language='en'):
    """
    Generate audio from text using Google TTS
    
    Args:
        text (str): Text to convert to speech
        language (str): Language code (en, hi, mr, ta, te, gu, pa, bn)
    
    Returns:
        dict: Audio information with URL
    """
    try:
        # Generate unique filename
        audio_id = str(uuid.uuid4())
        filename = f"{audio_id}.mp3"
        filepath = os.path.join('audio_files/generated', filename)
        
        # Create audio using gTTS
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(filepath)
        
        # Return audio URL
        audio_url = f"http://localhost:5000/api/audio/{filename}"
        
        return {
            "audio_url": audio_url,
            "audio_id": audio_id,
            "success": True,
            "message": "Audio generated successfully"
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error generating audio: {str(e)}"
        }
```

---

#### Step 6: Implement Translation Service

```python
# backend/services/translation_service.py
from googletrans import Translator

translator = Translator()

def translate_text(text, target_language='en'):
    """
    Translate text to target language
    
    Args:
        text (str): Text to translate
        target_language (str): Target language code
    
    Returns:
        str: Translated text
    """
    try:
        if target_language == 'en':
            return text
        
        result = translator.translate(text, dest=target_language)
        return result.text
        
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # Return original text if translation fails
```

---

### For Prathamesh (ML Developer)

#### Step 7: Implement ML Service

```python
# backend/services/ml_service.py
import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image
import cv2
from services.translation_service import translate_text

# Load trained model (do this once at startup)
MODEL_PATH = 'models/crop_disease_model.h5'
model = None

def load_model():
    """Load the trained model"""
    global model
    if model is None:
        try:
            model = keras.models.load_model(MODEL_PATH)
            print("Model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            model = None

# Load model at startup
load_model()

# Disease information database
DISEASE_INFO = {
    "Tomato_Early_Blight": {
        "name": "Tomato Early Blight",
        "description": "Early blight is a common fungal disease affecting tomato plants. It causes dark spots with concentric rings on leaves, leading to yellowing and defoliation. The disease thrives in warm, humid conditions.",
        "treatment": "Remove and destroy infected leaves immediately. Apply copper-based fungicide or chlorothalonil. Ensure proper plant spacing for air circulation. Avoid overhead watering. Rotate crops annually. Use disease-resistant varieties."
    },
    "Tomato_Late_Blight": {
        "name": "Tomato Late Blight",
        "description": "Late blight is a devastating disease caused by Phytophthora infestans. It causes water-soaked lesions on leaves and stems, leading to rapid plant death. Can destroy entire crops within days.",
        "treatment": "Apply fungicides containing mancozeb or chlorothalonil preventively. Remove infected plants immediately. Improve air circulation. Avoid working with wet plants. Use resistant varieties. Practice crop rotation."
    },
    "Potato_Late_Blight": {
        "name": "Potato Late Blight",
        "description": "Late blight affects potato plants causing dark lesions on leaves and tubers. The disease spreads rapidly in cool, wet conditions and can cause significant yield loss.",
        "treatment": "Apply protective fungicides before symptoms appear. Remove infected foliage. Ensure good drainage. Harvest tubers when fully mature. Store in cool, dry conditions. Use certified disease-free seed potatoes."
    },
    "Healthy": {
        "name": "Healthy Plant",
        "description": "The plant appears healthy with no visible signs of disease. Continue regular monitoring and maintenance practices.",
        "treatment": "Maintain current care routine. Ensure adequate watering, fertilization, and pest control. Monitor regularly for early disease detection."
    }
}

def preprocess_image(image_path, target_size=(224, 224)):
    """
    Preprocess image for model prediction
    
    Args:
        image_path (str): Path to image file
        target_size (tuple): Target image size
    
    Returns:
        numpy.ndarray: Preprocessed image array
    """
    try:
        # Load image
        img = Image.open(image_path)
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize image
        img = img.resize(target_size)
        
        # Convert to array
        img_array = np.array(img)
        
        # Normalize pixel values (0-1)
        img_array = img_array / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
        
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

def predict_disease(image_path, language='en'):
    """
    Predict disease from image
    
    Args:
        image_path (str): Path to uploaded image
        language (str): Language for response
    
    Returns:
        dict: Prediction result with disease info
    """
    try:
        # Preprocess image
        processed_image = preprocess_image(image_path)
        
        if processed_image is None:
            return {
                "error": "Failed to process image"
            }
        
        # Make prediction
        if model is not None:
            predictions = model.predict(processed_image)
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_idx])
            
            # Get class names (update based on your model)
            class_names = [
                "Tomato_Early_Blight",
                "Tomato_Late_Blight", 
                "Potato_Late_Blight",
                "Healthy"
            ]
            
            predicted_class = class_names[predicted_class_idx]
        else:
            # Fallback to mock prediction if model not loaded
            predicted_class = "Tomato_Early_Blight"
            confidence = 0.95
        
        # Get disease information
        disease_data = DISEASE_INFO.get(predicted_class, DISEASE_INFO["Healthy"])
        
        # Translate if needed
        disease_name = translate_text(disease_data["name"], language)
        description = translate_text(disease_data["description"], language)
        treatment = translate_text(disease_data["treatment"], language)
        
        # Prepare response
        result = {
            "disease_name": disease_name,
            "confidence": confidence,
            "description": description,
            "treatment": treatment,
            "language": language
        }
        
        return result
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return {
            "error": f"Prediction failed: {str(e)}"
        }
```

---

## 🚀 Running the Backend

### Start the Server

```bash
# Navigate to backend folder
cd backend

# Activate virtual environment
source venv/bin/activate  # Windows: venv\Scripts\activate

# Run Flask app
python app.py

# Server will start at http://localhost:5000
```

### Test the API

```bash
# Test health endpoint
curl http://localhost:5000/

# Test languages endpoint
curl http://localhost:5000/api/languages

# Test prediction endpoint (with image)
curl -X POST -F "image=@test_image.jpg" -F "language=en" \
  http://localhost:5000/api/predict
```

---

## 📱 Connecting Android App

### For Emulator
- Backend URL: `http://10.0.2.2:5000/`
- Already configured in `ApiClient.java`
- No changes needed

### For Real Device
1. Find your computer's IP address:
   ```bash
   # Windows
   ipconfig
   
   # Mac/Linux
   ifconfig
   ```

2. Update `ApiClient.java`:
   ```java
   private static final String BASE_URL = "http://YOUR_IP:5000/";
   ```

3. Ensure both devices are on same WiFi network

4. Allow firewall access to port 5000

---

## ✅ Testing Checklist

### Backend Testing
- [ ] Server starts without errors
- [ ] `/` endpoint returns status
- [ ] `/api/languages` returns language list
- [ ] `/api/predict` accepts image upload
- [ ] `/api/predict` returns valid JSON response
- [ ] `/api/tts/generate` creates audio file
- [ ] Audio files are accessible via URL
- [ ] CORS is enabled for Android app

### Integration Testing
- [ ] Android app connects to backend
- [ ] Image upload works from camera
- [ ] Disease prediction displays correctly
- [ ] Confidence score shows properly
- [ ] Language translation works
- [ ] Audio playback works
- [ ] Error handling works

---

## 🐛 Common Issues & Solutions

### Issue 1: Connection Refused
**Problem:** Android app can't connect to backend

**Solutions:**
- Check if backend server is running
- Verify correct IP address in `ApiClient.java`
- Ensure firewall allows port 5000
- Check if devices are on same network

### Issue 2: CORS Error
**Problem:** Browser/app blocked by CORS policy

**Solution:**
```python
from flask_cors import CORS
CORS(app)  # Add this to app.py
```

### Issue 3: Model Not Found
**Problem:** ML model file not loading

**Solutions:**
- Check model file path in `ml_service.py`
- Ensure model file exists in `models/` folder
- Verify model format (.h5 or .pkl)

### Issue 4: Audio Not Playing
**Problem:** Audio URL returns 404

**Solutions:**
- Check audio folder exists
- Verify file permissions
- Ensure correct URL format
- Check audio file was created

---

## 📊 Expected Data Flow

```
1. User captures image in Android app
   ↓
2. Image sent to POST /api/predict
   ↓
3. Backend receives image
   ↓
4. Prathamesh's ML model processes image
   ↓
5. Disease prediction generated
   ↓
6. Text translated to selected language
   ↓
7. Response sent back to Android app
   ↓
8. App displays results
   ↓
9. User clicks "Play Audio"
   ↓
10. Request sent to POST /api/tts/generate
   ↓
11. Audio file generated
   ↓
12. Audio URL returned
   ↓
13. App plays audio
```

---

## 📝 Quick Start Commands

```bash
# Setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
python app.py

# Test
curl http://localhost:5000/api/languages
```

---

## 🎯 Success Criteria

Backend is ready when:
- ✅ Server runs without errors
- ✅ All 3 endpoints respond correctly
- ✅ Android app receives real data
- ✅ Disease prediction works
- ✅ Audio generation works
- ✅ Multi-language support works

---

## 📞 Contact

**Questions?**
- Sohan (Mobile App) - Android implementation complete
- Pratham (Backend) - Implement API endpoints
- Prathamesh (ML) - Integrate trained model

---

**Good Luck! 🚀**

Once backend is running, the Android app will automatically fetch live data!
