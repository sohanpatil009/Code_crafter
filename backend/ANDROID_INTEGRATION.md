# 📱 Android App Integration Guide

## 🔌 Backend API for Android App

This backend is specifically designed to work with Sohan's Native Android app.

---

## 🌐 API Base URL

### For Android Emulator
```
http://10.0.2.2:5000/
```

### For Real Device (Same WiFi)
```
http://YOUR_COMPUTER_IP:5000/
```

To find your IP:
```bash
# Windows
ipconfig

# Mac/Linux
ifconfig | grep "inet "
```

---

## 📡 API Endpoints

### 1. Disease Prediction

**Endpoint:** `POST /api/predict`

**Request:**
```
Content-Type: multipart/form-data

Parameters:
- image: File (JPEG/PNG)
- language: String (en, hi, mr, ta, te, gu, pa, bn)
- user_id: String (optional)
```

**Response:**
```json
{
  "disease_name": "Tomato Early Blight",
  "confidence": 0.95,
  "description": "Early blight is a common fungal disease...",
  "treatment": "Remove infected leaves, apply fungicide...",
  "audio_url": "http://localhost:5000/api/audio/generated/abc123.mp3",
  "language": "en"
}
```

**Android Example:**
```java
// In ApiService.java
@Multipart
@POST("api/predict")
Call<DiseaseResult> predictDisease(
    @Part MultipartBody.Part image,
    @Part("language") RequestBody language
);

// Usage
File imageFile = new File(imagePath);
RequestBody requestFile = RequestBody.create(
    MediaType.parse("image/jpeg"), 
    imageFile
);
MultipartBody.Part imagePart = MultipartBody.Part.createFormData(
    "image", 
    imageFile.getName(), 
    requestFile
);
RequestBody languageBody = RequestBody.create(
    MediaType.parse("text/plain"), 
    "hi"
);

Call<DiseaseResult> call = apiService.predictDisease(imagePart, languageBody);
```

---

### 2. Text-to-Speech Generation

**Endpoint:** `POST /api/tts/generate`

**Request (JSON):**
```json
{
  "text": "टमाटर में अर्ली ब्लाइट रोग",
  "language": "hi"
}
```

**Request (Query Params):**
```
POST /api/tts/generate?text=Disease%20detected&language=en
```

**Response:**
```json
{
  "audio_url": "http://localhost:5000/api/audio/generated/xyz789.mp3",
  "audio_id": "xyz789",
  "success": true,
  "message": "Audio generated successfully"
}
```

**Android Example:**
```java
// In ApiService.java
@POST("api/tts/generate")
Call<AudioResponse> generateAudio(@Body AudioRequest request);

// Usage
AudioRequest request = new AudioRequest(diseaseText, "hi");
Call<AudioResponse> call = apiService.generateAudio(request);
```

---

### 3. Get Audio File

**Endpoint:** `GET /api/audio/generated/{filename}`

**Alternative:** `GET /api/tts/audio/{filename}`

**Response:** Audio file (MP3)

**Android Example:**
```java
// Play audio directly
MediaPlayer mediaPlayer = new MediaPlayer();
mediaPlayer.setDataSource(audioUrl);
mediaPlayer.prepare();
mediaPlayer.start();
```

---

### 4. Get Supported Languages

**Endpoint:** `GET /api/languages`

**Response:**
```json
{
  "success": true,
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

**Android Example:**
```java
// In ApiService.java
@GET("api/languages")
Call<LanguagesResponse> getLanguages();
```

---

## 🔧 Android App Configuration

### Update ApiClient.java

```java
public class ApiClient {
    // For Emulator
    private static final String BASE_URL = "http://10.0.2.2:5000/";
    
    // For Real Device (update with your IP)
    // private static final String BASE_URL = "http://192.168.1.100:5000/";
    
    private static Retrofit retrofit = null;
    
    public static Retrofit getClient() {
        if (retrofit == null) {
            retrofit = new Retrofit.Builder()
                    .baseUrl(BASE_URL)
                    .addConverterFactory(GsonConverterFactory.create())
                    .build();
        }
        return retrofit;
    }
}
```

---

## 🧪 Testing the Integration

### Step 1: Start Backend Server

```bash
cd backend
source venv/bin/activate
python app.py
```

Server should start at `http://0.0.0.0:5000`

### Step 2: Test Endpoints

```bash
# Test health
curl http://localhost:5000/

# Test languages
curl http://localhost:5000/api/languages

# Test prediction (with image)
curl -X POST -F "image=@test.jpg" -F "language=hi" \
  http://localhost:5000/api/predict

# Test TTS
curl -X POST -H "Content-Type: application/json" \
  -d '{"text":"Test message","language":"hi"}' \
  http://localhost:5000/api/tts/generate
```

### Step 3: Run Android App

1. Open Android Studio
2. Update `BASE_URL` in `ApiClient.java`
3. Run app on emulator or device
4. Capture image
5. Check if prediction works

---

## 🐛 Troubleshooting

### Issue: Connection Refused

**Symptoms:**
- Android app shows "Unable to connect"
- Network error in logs

**Solutions:**
1. Check backend server is running
2. Verify correct IP address
3. Ensure firewall allows port 5000
4. Check devices on same WiFi

**Test:**
```bash
# From your phone's browser, visit:
http://YOUR_IP:5000/api/languages
```

### Issue: Image Upload Fails

**Symptoms:**
- "No image provided" error
- Upload timeout

**Solutions:**
1. Check image size (max 16MB)
2. Verify file format (JPG/PNG)
3. Check multipart form data format
4. Increase timeout in Retrofit

### Issue: Audio Not Playing

**Symptoms:**
- Audio URL returns 404
- No sound plays

**Solutions:**
1. Check audio file was created
2. Verify audio folder exists
3. Check file permissions
4. Test audio URL in browser

### Issue: Translation Not Working

**Symptoms:**
- English text returned for Hindi
- Translation errors

**Solutions:**
1. Check internet connection (googletrans needs internet)
2. Verify language code is correct
3. Check googletrans version
4. Try alternative translation library

---

## 📊 Data Flow

```
Android App (Sohan)
    ↓
    📸 Capture Image
    ↓
    📤 Upload to /api/predict
    ↓
Backend API (Pratham)
    ↓
    🖼️ Preprocess Image
    ↓
ML Model (Prathamesh)
    ↓
    🤖 Predict Disease
    ↓
Backend API
    ↓
    🌐 Translate to Language
    ↓
    📤 Return Result
    ↓
Android App
    ↓
    📱 Display Result
    ↓
    🔊 Play Audio (if requested)
```

---

## ✅ Integration Checklist

### Backend (Pratham)
- [x] Flask server running
- [x] CORS enabled
- [x] All endpoints working
- [x] ML model integrated
- [x] TTS service working
- [x] Translation working
- [x] Audio files accessible
- [x] Error handling implemented

### Android App (Sohan)
- [ ] BASE_URL configured
- [ ] Retrofit client setup
- [ ] Image upload working
- [ ] API calls implemented
- [ ] Response parsing working
- [ ] UI displays results
- [ ] Audio playback working
- [ ] Error handling implemented

---

## 🚀 Quick Test Script

Save as `test_api.sh`:

```bash
#!/bin/bash

BASE_URL="http://localhost:5000"

echo "Testing Crop Disease Detection API..."
echo ""

echo "1. Testing health endpoint..."
curl -s $BASE_URL/ | jq
echo ""

echo "2. Testing languages endpoint..."
curl -s $BASE_URL/api/languages | jq
echo ""

echo "3. Testing TTS endpoint..."
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"text":"Test message","language":"hi"}' \
  $BASE_URL/api/tts/generate | jq
echo ""

echo "4. Testing prediction endpoint (need image)..."
echo "Run: curl -X POST -F 'image=@test.jpg' -F 'language=hi' $BASE_URL/api/predict"
echo ""

echo "✅ API tests complete!"
```

Run with:
```bash
chmod +x test_api.sh
./test_api.sh
```

---

## 📞 Support

**Backend Issues:** Contact Pratham
**Android Issues:** Contact Sohan
**ML Model Issues:** Contact Prathamesh

---

## 🎯 Success Criteria

Integration is successful when:

1. ✅ Android app connects to backend
2. ✅ Image upload works
3. ✅ Disease prediction displays
4. ✅ Confidence score shows
5. ✅ Language translation works
6. ✅ Audio plays correctly
7. ✅ Error messages display properly
8. ✅ App works on both emulator and device

---

**Happy Integrating! 🚀**
