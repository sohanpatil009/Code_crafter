# Crop Disease Detection - Backend API

Backend API for Crop Disease Detection Platform with ML integration, TTS, and multi-language support.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MongoDB or PostgreSQL
- pip (Python package manager)

### Installation

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run the server**
```bash
python app.py
```

Server will start at `http://localhost:5000`

## 📋 API Endpoints

### Health Check
```
GET /api/health
```

### Disease Prediction
```
POST /api/predict
Content-Type: multipart/form-data

Parameters:
- image: Image file (required)
- language: Language code (optional, default: 'en')
- user_id: User identifier (optional)
```

### Text-to-Speech
```
POST /api/tts/generate
Content-Type: application/json

Body:
{
  "text": "Disease information text",
  "language": "hi"
}
```

### Get Audio File
```
GET /api/tts/audio/<filename>
```

### Translation
```
POST /api/translate
Content-Type: application/json

Body:
{
  "text": "Text to translate",
  "target_lang": "hi",
  "source_lang": "en"
}
```

### Get Supported Languages
```
GET /api/languages
```

### Set Language Preference
```
POST /api/language/preference
Content-Type: application/json

Body:
{
  "user_id": "user123",
  "language": "hi"
}
```

### Get Prediction History
```
GET /api/history?user_id=user123&limit=50
```

### Get All Diseases
```
GET /api/diseases
```

### Get Disease Details
```
GET /api/disease/<disease_name>?language=hi
```

### Submit Feedback
```
POST /api/feedback
Content-Type: application/json

Body:
{
  "prediction_id": "123",
  "feedback": "Correct prediction"
}
```

## 🌐 Supported Languages

- Hindi (hi)
- English (en)
- Marathi (mr)
- Tamil (ta)
- Telugu (te)
- Gujarati (gu)
- Punjabi (pa)
- Bengali (bn)

## 🗂️ Project Structure

```
backend/
├── api/
│   ├── __init__.py
│   ├── routes.py          # API endpoints
│   ├── middleware.py      # Request/response middleware
│   └── validators.py      # Input validation
├── services/
│   ├── ml_service.py      # ML model inference
│   ├── tts_service.py     # Text-to-speech
│   └── translation_service.py  # Translation
├── database/
│   ├── connection.py      # Database connection
│   ├── models.py          # Data models
│   └── queries.py         # Database queries
├── uploads/               # Uploaded images
├── audio_files/
│   └── generated/         # Generated audio files
├── config.py              # Configuration
├── app.py                 # Application entry point
├── requirements.txt       # Dependencies
└── README.md
```

## 🔧 Configuration

Edit `.env` file:

```env
# Flask
SECRET_KEY=your-secret-key
DEBUG=True
HOST=0.0.0.0
PORT=5000

# Database
DATABASE_TYPE=mongodb
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB=crop_disease_db

# TTS
TTS_ENGINE=gtts  # or pyttsx3
```

## 🧪 Testing

Test the API using curl:

```bash
# Health check
curl http://localhost:5000/api/health

# Predict disease
curl -X POST http://localhost:5000/api/predict \
  -F "image=@/path/to/image.jpg" \
  -F "language=hi"

# Generate TTS
curl -X POST http://localhost:5000/api/tts/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "टमाटर में अर्ली ब्लाइट रोग", "language": "hi"}'
```

## 📦 Dependencies

- **Flask** - Web framework
- **TensorFlow** - ML model inference
- **OpenCV** - Image processing
- **gTTS** - Text-to-speech
- **googletrans** - Translation
- **MongoDB/PostgreSQL** - Database

## 🚀 Deployment

### Using Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker
```bash
docker build -t crop-disease-api .
docker run -p 5000:5000 crop-disease-api
```

## 👨‍💻 Developer

**Pratham** - Backend Development & API Integration

## 📝 Notes

- ML model file should be placed at `../trained_models/crop_disease_model.h5`
- If model is not found, API will use mock predictions for testing
- Audio files are automatically generated and stored
- CORS is enabled for all origins (configure for production)

## 🤝 Integration

This backend integrates with:
- **Prathamesh's ML Model** - Disease prediction
- **Sohan's Android App** - Mobile client
- **Shravani's UI/UX** - Design specifications

---

**Happy Coding! 🌱**
