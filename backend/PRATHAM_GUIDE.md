# 👨‍💻 Pratham's Backend Development Guide

## 📋 Your Responsibilities

As the **Backend Developer**, you are responsible for:

1. ✅ **API Development** - All REST API endpoints
2. ✅ **Database Integration** - MongoDB/PostgreSQL setup and queries
3. ✅ **ML Model Integration** - Connect Prathamesh's model to API
4. ✅ **TTS Service** - Text-to-speech audio generation
5. ✅ **Translation Service** - Multi-language support
6. ✅ **API Documentation** - Swagger/OpenAPI docs
7. ✅ **Deployment** - Server deployment and configuration

---

## 🎯 What's Already Done

### ✅ Complete Backend Structure Created

```
backend/
├── api/
│   ├── routes.py          ✅ All API endpoints implemented
│   ├── middleware.py      ✅ Request logging and error handling
│   └── validators.py      ✅ Input validation functions
│
├── services/
│   ├── ml_service.py      ✅ ML model inference service
│   ├── tts_service.py     ✅ Text-to-speech (gTTS + pyttsx3)
│   └── translation_service.py  ✅ Multi-language translation
│
├── database/
│   ├── connection.py      ✅ MongoDB & PostgreSQL connection
│   ├── models.py          ✅ Data models
│   └── queries.py         ✅ Database operations
│
├── config.py              ✅ Configuration management
├── app.py                 ✅ Flask application
├── requirements.txt       ✅ All dependencies
├── seed_data.py          ✅ Sample disease data
├── postman_collection.json ✅ API testing collection
└── run.sh                ✅ Quick start script
```

---

## 🚀 Quick Start

### 1. Setup Environment

```bash
cd backend
./run.sh
```

Or manually:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run server
python app.py
```

### 2. Seed Database (Optional)

```bash
python seed_data.py
```

### 3. Test API

```bash
# Health check
curl http://localhost:5000/api/health

# Get languages
curl http://localhost:5000/api/languages
```

---

## 📡 API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| POST | `/api/predict` | Upload image & predict disease |
| POST | `/api/tts/generate` | Generate audio from text |
| GET | `/api/tts/audio/<filename>` | Get audio file |
| POST | `/api/translate` | Translate text |
| GET | `/api/languages` | Get supported languages |
| POST | `/api/language/preference` | Set user language |
| GET | `/api/history` | Get prediction history |
| GET | `/api/diseases` | Get all diseases |
| GET | `/api/disease/<name>` | Get disease details |
| POST | `/api/feedback` | Submit feedback |

---

## 🔗 Integration Points

### With Prathamesh (ML Developer)

**What you need from him:**
- Trained model file: `crop_disease_model.h5`
- Model input size (currently set to 224x224)
- List of disease classes
- Image preprocessing requirements

**What you provide to him:**
- `services/ml_service.py` - ML inference wrapper
- Image preprocessing pipeline
- API endpoint for predictions

**Integration:**
```python
# In ml_service.py
self.model = tf.keras.models.load_model(Config.MODEL_PATH)
predictions = self.model.predict(processed_image)
```

### With Sohan (Android Developer)

**What he needs from you:**
- API base URL
- All endpoint documentation
- Request/response formats
- Error codes and messages
- Postman collection

**What you need from him:**
- User authentication (if implemented)
- Device/user identification
- Image quality requirements

**Example Android API Call:**
```java
// POST /api/predict
MultipartBody.Part imagePart = ...;
RequestBody language = RequestBody.create("hi", MediaType.parse("text/plain"));
Call<PredictionResponse> call = apiService.predictDisease(imagePart, language);
```

---

## 🔧 Configuration

### Environment Variables (.env)

```env
# Flask
SECRET_KEY=your-secret-key-here
DEBUG=True
HOST=0.0.0.0
PORT=5000

# Database
DATABASE_TYPE=mongodb
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB=crop_disease_db

# TTS
TTS_ENGINE=gtts  # or pyttsx3 for offline
```

### Supported Languages

```python
SUPPORTED_LANGUAGES = {
    'hi': 'Hindi',
    'en': 'English',
    'mr': 'Marathi',
    'ta': 'Tamil',
    'te': 'Telugu',
    'gu': 'Gujarati',
    'pa': 'Punjabi',
    'bn': 'Bengali'
}
```

---

## 🧪 Testing

### Using Postman
1. Import `postman_collection.json`
2. Set `base_url` variable to `http://localhost:5000`
3. Test all endpoints

### Using curl

```bash
# Predict disease
curl -X POST http://localhost:5000/api/predict \
  -F "image=@test_image.jpg" \
  -F "language=hi" \
  -F "user_id=user123"

# Generate TTS
curl -X POST http://localhost:5000/api/tts/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "टमाटर में रोग", "language": "hi"}'

# Translate
curl -X POST http://localhost:5000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Disease detected", "target_lang": "hi"}'
```

---

## 📝 Next Steps

### Immediate Tasks

1. **Test the API**
   - Run the server
   - Test all endpoints
   - Verify responses

2. **Database Setup**
   - Install MongoDB or PostgreSQL
   - Run seed script
   - Test database queries

3. **ML Model Integration**
   - Get model file from Prathamesh
   - Place in `../trained_models/`
   - Test predictions

4. **TTS Testing**
   - Test both gTTS and pyttsx3
   - Verify audio generation
   - Test all languages

### Future Enhancements

- [ ] Add authentication (JWT)
- [ ] Implement rate limiting
- [ ] Add caching (Redis)
- [ ] Create Swagger documentation
- [ ] Add logging system
- [ ] Implement file cleanup
- [ ] Add monitoring (Prometheus)
- [ ] Create Docker container
- [ ] Setup CI/CD pipeline

---

## 🐛 Troubleshooting

### Common Issues

**1. Module not found**
```bash
# Make sure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**2. Database connection error**
```bash
# Check if MongoDB is running
sudo systemctl status mongod

# Or start it
sudo systemctl start mongod
```

**3. Model not found**
```bash
# Create directory and add placeholder
mkdir -p ../trained_models
# Get actual model from Prathamesh
```

**4. TTS not working**
```bash
# For pyttsx3 on Linux
sudo apt-get install espeak

# For audio playback
sudo apt-get install ffmpeg
```

---

## 📚 Resources

### Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [TensorFlow Guide](https://www.tensorflow.org/guide)
- [MongoDB Python Driver](https://pymongo.readthedocs.io/)
- [gTTS Documentation](https://gtts.readthedocs.io/)

### Useful Commands

```bash
# Check Python version
python --version

# List installed packages
pip list

# Freeze dependencies
pip freeze > requirements.txt

# Run with Gunicorn (production)
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Check port usage
lsof -i :5000
```

---

## 🤝 Team Communication

### Daily Standup Points
- API endpoints completed
- Integration issues
- Blockers (waiting for model, etc.)
- Testing status

### Code Review Checklist
- [ ] All endpoints tested
- [ ] Error handling implemented
- [ ] Input validation added
- [ ] Documentation updated
- [ ] Code commented
- [ ] No hardcoded values

---

## 🎯 Success Criteria

Your backend is ready when:

1. ✅ All API endpoints working
2. ✅ Database connected and seeded
3. ✅ ML model integrated (or mock working)
4. ✅ TTS generating audio
5. ✅ Translation working for all languages
6. ✅ Postman collection tested
7. ✅ Android app can connect
8. ✅ Error handling robust
9. ✅ Documentation complete
10. ✅ Ready for deployment

---

## 💡 Tips

1. **Start Simple**: Test with mock data first, then integrate real ML model
2. **Log Everything**: Use print statements for debugging
3. **Test Incrementally**: Test each endpoint as you build
4. **Version Control**: Commit frequently with clear messages
5. **Ask for Help**: Coordinate with Prathamesh for ML integration
6. **Document**: Keep API docs updated for Sohan

---

## 📞 Contact Points

- **Prathamesh**: ML model, image processing questions
- **Sohan**: API requirements, Android integration
- **Shravani**: UI/UX feedback, testing

---

**Good luck, Pratham! You've got this! 🚀**

All the backend structure is ready. Now just:
1. Test it
2. Integrate the ML model
3. Connect with the Android app
4. Deploy!

**Happy Coding! 💻**
