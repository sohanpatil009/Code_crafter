# Crop Disease Detection Platform

A comprehensive image processing platform built with Python to detect and classify crop diseases using machine learning and computer vision techniques.

## 👥 Team Members

- **Sohan** - Mobile App Development (Native Android - Java)
- **Pratham** - Backend Development & API Integration
- **Prathamesh** - Machine Learning Model Development & Image Processing
- **Shravani** - UI/UX Design & Testing

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Mobile App Layer                          │
│         (Native Android Java - Camera Integration)         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    API Gateway Layer                        │
│              (Python Flask/FastAPI REST API)                │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  Business Logic Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Image        │  │ ML Model     │  │ Disease      │     │
│  │ Preprocessing│  │ Inference    │  │ Database     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Image        │  │ Trained      │  │ Disease      │     │
│  │ Storage      │  │ Models       │  │ Metadata     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Core Technologies
- **Python 3.8+** - Backend and ML development
- **TensorFlow/Keras** - Deep learning framework
- **OpenCV** - Image processing and computer vision
- **NumPy & Pandas** - Data manipulation and analysis
- **Scikit-learn** - Machine learning utilities

### Backend Framework
- **Flask/FastAPI** - REST API development
- **Python** - Backend logic and ML inference

### Mobile App
- **Java** - Native Android development language
- **Android SDK** - Android app development framework
- **CameraX** - Modern camera integration library
- **Material Design 3** - UI components and design system
- **Retrofit/OkHttp** - HTTP client for API communication
- **Navigation Component** - Fragment navigation

### Database
- **MongoDB/PostgreSQL** - Disease records and metadata
- **AWS S3/Local Storage** - Image storage

### ML/DL Libraries
- **PIL/Pillow** - Image manipulation
- **Matplotlib/Seaborn** - Visualization
- **Albumentations** - Image augmentation

### Text-to-Speech & Translation
- **gTTS (Google Text-to-Speech)** - Convert text to speech
- **pyttsx3** - Offline TTS engine
- **Google Translate API** - Multi-language translation
- **Googletrans** - Language translation library
- **langdetect** - Language detection

### Deployment
- **Docker** - Containerization
- **Gunicorn/Uvicorn** - WSGI/ASGI server
- **Nginx** - Reverse proxy

---

## 📦 Core Modules

### 1. Image Preprocessing Module
**Responsibilities:**
- Image upload and validation
- Resize and normalize images
- Noise reduction and enhancement
- Color space conversion
- Data augmentation

**Key Files:**
- `preprocessing/image_loader.py`
- `preprocessing/augmentation.py`
- `preprocessing/normalization.py`

---

### 2. Feature Extraction Module
**Responsibilities:**
- Extract relevant features from images
- Edge detection and segmentation
- Texture analysis
- Color histogram analysis

**Key Files:**
- `features/extractor.py`
- `features/segmentation.py`
- `features/texture_analysis.py`

---

### 3. Machine Learning Module
**Responsibilities:**
- CNN model architecture (ResNet, VGG, MobileNet)
- Model training and validation
- Transfer learning implementation
- Model evaluation and metrics

**Key Files:**
- `models/cnn_model.py`
- `models/train.py`
- `models/evaluate.py`
- `models/predict.py`

---

### 4. Disease Classification Module
**Responsibilities:**
- Disease prediction from processed images
- Confidence score calculation
- Multi-class classification
- Disease information retrieval

**Key Files:**
- `classification/predictor.py`
- `classification/disease_info.py`
- `classification/confidence_scorer.py`

---

### 5. Backend API Module
**Responsibilities:**
- RESTful API endpoints
- Request validation
- Response formatting
- Error handling
- ML model integration
- TTS and translation services

**Key Files:**
- `backend/api/routes.py`
- `backend/api/middleware.py`
- `backend/api/validators.py`
- `backend/services/ml_service.py`

---

### 6. Mobile App Module (Native Android Java)
**Responsibilities:**
- CameraX integration for real camera capture
- Image upload to backend API
- Display prediction results with confidence scores
- Audio playback for TTS
- Language selection (8 Indian languages)
- Material Design 3 UI
- Fragment-based navigation

**Key Files:**
- `mobile_app/app/src/main/java/com/cropdetection/app/MainActivity.java`
- `mobile_app/app/src/main/java/com/cropdetection/app/ui/CameraFragment.java`
- `mobile_app/app/src/main/java/com/cropdetection/app/ui/ResultsFragment.java`
- `mobile_app/app/src/main/java/com/cropdetection/app/api/ApiClient.java`
- `mobile_app/app/src/main/java/com/cropdetection/app/api/DiseaseResult.java`

---

### 7. Database Module
**Responsibilities:**
- Store disease metadata
- User history tracking
- Model performance logs
- Image metadata storage

**Key Files:**
- `database/models.py`
- `database/connection.py`
- `database/queries.py`

---

### 8. Text-to-Speech Module
**Responsibilities:**
- Convert disease information to speech
- Support multiple languages (Hindi, English, Marathi, etc.)
- Audio file generation and streaming
- Voice customization options

**Key Files:**
- `tts/speech_engine.py`
- `tts/audio_generator.py`
- `tts/language_config.py`

---

### 9. Multi-Language Module
**Responsibilities:**
- Translate disease information to multiple languages
- Language detection and selection
- Support for regional languages
- Localization of UI text

**Key Files:**
- `translation/translator.py`
- `translation/language_data.py`
- `translation/localization.py`

---

## 📋 Work Distribution

### 🔹 Sohan - Mobile App Development (Native Android Java)
**Tasks:**
- Set up Native Android project with Java
- Implement CameraX integration for real camera capture
- Build image upload functionality to backend API
- Create results display screen with disease information
- Implement audio player for TTS playback
- Add language selector component (8 Indian languages)
- Design Material Design 3 UI
- Handle API communication and error states
- Implement fragment navigation
- Test on Android devices

**Deliverables:**
- `mobile_app/` complete Native Android Java project
- CameraX camera capture module
- API client implementation with mock data
- UI components (MainActivity, CameraFragment, ResultsFragment)
- Language selector with 8 languages
- Mobile app documentation
- APK build files

---

### 🔹 Pratham - Backend Development & API Integration
**Tasks:**
- Set up Flask/FastAPI project structure
- Develop REST API endpoints (upload, predict, history)
- Implement request validation and error handling
- Database integration and CRUD operations
- **Integrate ML model inference in API**
- **Implement TTS API endpoints**
- **Implement translation API endpoints**
- **Audio file generation and streaming**
- **Language preference management**
- API documentation using Swagger/OpenAPI
- Authentication and authorization (if needed)
- Deploy backend server

**Deliverables:**
- `backend/api/` module
- `backend/database/` module
- `backend/services/` (TTS, Translation, ML inference)
- API documentation
- Postman collection for testing
- Deployment scripts

---

### 🔹 Prathamesh - Machine Learning & Image Processing
**Tasks:**
- Research and select appropriate CNN architecture
- Collect and prepare training dataset
- **Implement image preprocessing pipeline**
- **Develop feature extraction algorithms**
- **Image segmentation for leaf detection**
- Implement transfer learning (ResNet50/MobileNet)
- Train and fine-tune the model
- Model evaluation and optimization
- **Data augmentation techniques**
- Save trained models in appropriate format
- **Integration with backend API**

**Deliverables:**
- `models/` module
- `preprocessing/` module
- `features/` module
- Trained model files (.h5, .pkl)
- Training notebooks
- Model performance report
- Image processing utilities
- Model API integration code

---

### 🔹 Shravani - UI/UX Design & Testing
**Tasks:**
- Design mobile app UI/UX mockups and wireframes
- Create user flow diagrams
- Design color schemes and branding
- Create icons and graphics for the app
- Design disease information cards layout
- Plan language selector interface
- Design audio player controls
- User testing and feedback collection
- Create user documentation and help guides
- Test app on different devices
- Accessibility testing

**Deliverables:**
- UI/UX mockups (Figma/Adobe XD)
- Design system and style guide
- User flow diagrams
- App icons and graphics
- User documentation
- Testing reports
- Feedback and improvement suggestions

---

## 🚀 Project Structure

```
crop-disease-detection/
│
├── backend/                          # Python Backend (Pratham)
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── middleware.py
│   │   └── validators.py
│   │
│   ├── models/                       # ML Models (Prathamesh)
│   │   ├── __init__.py
│   │   ├── cnn_model.py
│   │   ├── train.py
│   │   ├── evaluate.py
│   │   └── predict.py
│   │
│   ├── preprocessing/                # Image Processing (Prathamesh)
│   │   ├── __init__.py
│   │   ├── image_loader.py
│   │   ├── augmentation.py
│   │   └── normalization.py
│   │
│   ├── features/                     # Feature Extraction (Prathamesh)
│   │   ├── __init__.py
│   │   ├── extractor.py
│   │   ├── segmentation.py
│   │   └── texture_analysis.py
│   │
│   ├── services/                     # Backend Services (Pratham)
│   │   ├── __init__.py
│   │   ├── ml_service.py
│   │   ├── tts_service.py
│   │   └── translation_service.py
│   │
│   ├── database/                     # Database (Pratham)
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── connection.py
│   │   └── queries.py
│   │
│   ├── audio_files/
│   │   └── generated/
│   │
│   ├── requirements.txt
│   ├── config.py
│   └── app.py
│
├── mobile_app/                       # Native Android Java App (Sohan)
│   ├── app/
│   │   ├── src/
│   │   │   └── main/
│   │   │       ├── java/com/cropdetection/app/
│   │   │       │   ├── MainActivity.java
│   │   │       │   ├── ui/
│   │   │       │   │   ├── CameraFragment.java
│   │   │       │   │   └── ResultsFragment.java
│   │   │       │   └── api/
│   │   │       │       ├── ApiClient.java
│   │   │       │       └── DiseaseResult.java
│   │   │       ├── res/
│   │   │       │   ├── layout/
│   │   │       │   └── values/
│   │   │       └── AndroidManifest.xml
│   │   └── build.gradle.kts
│   │
│   ├── build.gradle.kts
│   ├── settings.gradle.kts
│   ├── gradle.properties
│   └── README.md
│
├── trained_models/                   # Trained Models (Prathamesh)
│   └── crop_disease_model.h5
│
├── data/                             # Training Data (Prathamesh)
│   ├── train/
│   ├── test/
│   └── validation/
│
├── design/                           # UI/UX Assets (Shravani)
│   ├── mockups/
│   ├── wireframes/
│   ├── icons/
│   └── style_guide.md
│
├── notebooks/                        # ML Notebooks (Prathamesh)
│   └── model_training.ipynb
│
├── tests/
│   ├── test_api.py
│   ├── test_preprocessing.py
│   ├── test_model.py
│   └── test_mobile_app.rs
│
└── README.md
```

---

## 📥 Installation

### Backend Setup (Pratham)
```bash
# Clone the repository
git clone <repository-url>
cd crop-disease-detection/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# For TTS support (optional - for offline TTS)
# Windows
pip install pipwin
pipwin install pyaudio

# Linux/Mac
sudo apt-get install espeak
sudo apt-get install ffmpeg

# Run backend server
python app.py
```

### Mobile App Setup (Sohan)
```bash
# Prerequisites
# - Android Studio installed
# - Android SDK (API 24+)
# - Java JDK 17+

# Navigate to mobile app
cd crop-disease-detection/mobile_app

# Build the app
gradlew build

# For Android build (APK)
gradlew assembleDebug

# Install on connected device
gradlew installDebug

# Or open in Android Studio and run
```

---

## 🎯 Key Features

1. **Image Upload** - Support for multiple image formats (JPG, PNG)
2. **Real-time Detection** - Fast disease classification
3. **Confidence Scoring** - Prediction confidence percentage
4. **Disease Information** - Detailed info about detected diseases
5. **🔊 Text-to-Speech** - Audio playback of disease information
6. **🌐 Multi-Language Support** - Hindi, English, Marathi, Tamil, Telugu, Gujarati
7. **Audio Controls** - Play, pause, stop, and download audio
8. **Language Switcher** - Easy language selection
9. **History Tracking** - User prediction history
10. **Multi-crop Support** - Support for various crop types
11. **Responsive Design** - Works on desktop and mobile
12. **Offline TTS** - Works without internet using pyttsx3

---

## � Text-to-Speech & Multi-Language Features

### Supported Languages
- 🇮🇳 **Hindi (हिंदी)**
- 🇬🇧 **English**
- 🇮🇳 **Marathi (मराठी)**
- 🇮🇳 **Tamil (தமிழ்)**
- 🇮🇳 **Telugu (తెలుగు)**
- 🇮🇳 **Gujarati (ગુજરાતી)**
- 🇮🇳 **Punjabi (ਪੰਜਾਬੀ)**
- 🇮🇳 **Bengali (বাংলা)**

### TTS Implementation Options

#### Option 1: Google TTS (gTTS) - Online
```python
from gtts import gTTS
import os

def generate_audio(text, language='hi'):
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save("disease_info.mp3")
    return "disease_info.mp3"
```

#### Option 2: pyttsx3 - Offline
```python
import pyttsx3

def speak_text(text, language='hindi'):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)
    engine.say(text)
    engine.runAndWait()
```

### Translation Implementation
```python
from googletrans import Translator

def translate_disease_info(text, target_lang='hi'):
    translator = Translator()
    translated = translator.translate(text, dest=target_lang)
    return translated.text
```

### Language Codes
- Hindi: `hi`
- English: `en`
- Marathi: `mr`
- Tamil: `ta`
- Telugu: `te`
- Gujarati: `gu`
- Punjabi: `pa`
- Bengali: `bn`

### User Flow with TTS
1. User uploads crop image
2. System detects disease
3. Disease information displayed in selected language
4. 🔊 Audio button appears
5. User clicks to hear information
6. TTS speaks disease details in chosen language

---

## 📊 Supported Diseases (Example)

- Tomato Early Blight
- Tomato Late Blight
- Potato Late Blight
- Corn Common Rust
- Apple Scab
- Grape Black Rot
- And more...

---

## 🔄 Development Workflow

1. **Week 1-2**: Setup & Architecture
   - **Sohan**: Native Android project setup, CameraX integration
   - **Pratham**: Backend Flask/FastAPI setup, database design
   - **Prathamesh**: Dataset collection, preprocessing pipeline setup
   - **Shravani**: UI/UX mockups, design system creation

2. **Week 3-4**: Core Development
   - **Sohan**: Android app UI, camera capture with CameraX, API client
   - **Pratham**: API endpoints, TTS/translation integration
   - **Prathamesh**: Model training, image processing implementation
   - **Shravani**: User testing, feedback collection

3. **Week 5**: Integration
   - **Sohan + Pratham**: Android app ↔ Backend API integration
   - **Pratham + Prathamesh**: ML model ↔ API integration
   - **All**: End-to-end testing

4. **Week 6**: Deployment & Documentation
   - **Sohan**: Android app build (APK)
   - **Pratham**: Backend deployment (AWS/Heroku)
   - **Prathamesh**: Model optimization and documentation
   - **Shravani**: User documentation and guides

---

## 🧪 Testing

```bash
# Run unit tests
pytest tests/

# Run API tests
pytest tests/test_api.py

# Test model accuracy
python models/evaluate.py
```

---

## 📝 API Endpoints

```
POST   /api/predict              - Upload image and get prediction
GET    /api/diseases             - Get list of all diseases
GET    /api/disease/:id          - Get disease details
GET    /api/history              - Get prediction history
POST   /api/feedback             - Submit feedback

# TTS & Translation Endpoints
POST   /api/tts/generate         - Generate audio from text
GET    /api/tts/audio/:id        - Stream/download audio file
POST   /api/translate            - Translate disease info
GET    /api/languages            - Get supported languages
POST   /api/language/preference  - Set user language preference
```

---

## 🤝 Contributing

Each team member should:
1. Create feature branches from `main`
2. Follow naming convention: 
   - `android/feature-name` (Sohan)
   - `backend/feature-name` (Pratham)
   - `ml/feature-name` (Prathamesh)
   - `design/feature-name` (Shravani)
3. Write clean, documented code
4. Test before pushing
5. Create pull requests for review

### Branch Structure
- `main` - Production ready code
- `develop` - Development branch
- `android/*` - Android app features (Sohan)
- `backend/*` - Backend features (Pratham)
- `ml/*` - ML and image processing (Prathamesh)
- `design/*` - Design assets (Shravani)

---

## 📄 License

This project is developed as part of academic coursework.

---

## 📞 Contact

For queries, reach out to team members:
- **Sohan** - Mobile App (Native Android Java)
- **Pratham** - Backend & API
- **Prathamesh** - ML Models & Image Processing
- **Shravani** - UI/UX Design & Testing

---

**Happy Coding! 🌱🔬**
