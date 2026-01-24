# Crop Disease Detection - Android App

Native Android application built with Java for detecting crop diseases using machine learning.

## 🚀 Features

- **CameraX Integration** - Real camera capture with modern CameraX API
- **Disease Detection** - Upload images to backend API for ML-based disease detection
- **Multi-Language Support** - 8 Indian languages (Hindi, Marathi, Tamil, Telugu, Gujarati, Punjabi, Bengali, English)
- **Text-to-Speech** - Audio playback of disease information in selected language
- **Material Design 3** - Modern UI with Material Design components
- **Fragment Navigation** - Smooth navigation between camera and results screens

## 📱 Screenshots

### Camera Screen
- Real-time camera preview using CameraX
- Capture button to take photos
- Loading indicator during upload

### Results Screen
- Captured image display
- Disease name and confidence score
- Detailed description and treatment information
- Language selector dropdown
- Audio playback controls
- Back to camera button

## 🛠️ Tech Stack

- **Language**: Java
- **Min SDK**: 24 (Android 7.0)
- **Target SDK**: 34 (Android 14)
- **Build System**: Gradle with Kotlin DSL

### Key Libraries

- **CameraX** (1.3.1) - Camera integration
- **Retrofit** (2.9.0) - REST API client
- **Gson** (2.10.1) - JSON parsing
- **Material Components** (1.11.0) - UI components
- **Navigation Component** (2.7.6) - Fragment navigation
- **Glide** (4.16.0) - Image loading

## 📦 Project Structure

```
mobile_app/
├── app/
│   ├── src/main/
│   │   ├── java/com/cropdetection/app/
│   │   │   ├── MainActivity.java
│   │   │   ├── api/
│   │   │   │   ├── ApiClient.java
│   │   │   │   ├── ApiService.java
│   │   │   │   ├── DiseaseResult.java
│   │   │   │   ├── AudioResponse.java
│   │   │   │   └── LanguagesResponse.java
│   │   │   └── ui/
│   │   │       ├── CameraFragment.java
│   │   │       └── ResultsFragment.java
│   │   ├── res/
│   │   │   ├── layout/
│   │   │   │   ├── activity_main.xml
│   │   │   │   ├── fragment_camera.xml
│   │   │   │   └── fragment_results.xml
│   │   │   ├── navigation/
│   │   │   │   └── nav_graph.xml
│   │   │   └── values/
│   │   │       ├── strings.xml
│   │   │       ├── colors.xml
│   │   │       └── themes.xml
│   │   └── AndroidManifest.xml
│   └── build.gradle.kts
├── build.gradle.kts
├── settings.gradle.kts
└── gradle.properties
```

## 🔧 Setup Instructions

### Prerequisites

- Android Studio (latest version)
- JDK 17 or higher
- Android SDK (API 24+)
- Physical Android device or emulator

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd crop-disease-detection/mobile_app
   ```

2. **Open in Android Studio**
   - Open Android Studio
   - Select "Open an Existing Project"
   - Navigate to `mobile_app` folder
   - Wait for Gradle sync to complete

3. **Configure API Base URL**
   - Open `ApiClient.java`
   - Update `BASE_URL`:
     - For emulator: `http://10.0.2.2:5000/`
     - For real device: `http://YOUR_IP_ADDRESS:5000/`

4. **Build the project**
   ```bash
   ./gradlew build
   ```

5. **Run on device/emulator**
   - Connect Android device via USB (enable USB debugging)
   - Or start Android emulator
   - Click "Run" in Android Studio

## 📱 Building APK

### Debug APK
```bash
./gradlew assembleDebug
```
Output: `app/build/outputs/apk/debug/app-debug.apk`

### Release APK
```bash
./gradlew assembleRelease
```
Output: `app/build/outputs/apk/release/app-release.apk`

## 🔑 Permissions

The app requires the following permissions:

- **CAMERA** - For capturing crop images
- **INTERNET** - For API communication
- **ACCESS_NETWORK_STATE** - For checking network connectivity

## 🌐 API Integration

### Endpoints Used

1. **POST /api/predict**
   - Upload image for disease detection
   - Parameters: `image` (multipart), `language` (string)
   - Response: `DiseaseResult` object

2. **POST /api/tts/generate**
   - Generate audio from text
   - Parameters: `text`, `language`
   - Response: `AudioResponse` with audio URL

3. **GET /api/languages**
   - Get supported languages
   - Response: List of language objects

### Mock Data

The app includes mock data for testing without backend:
- Sample disease: "Tomato Early Blight"
- Confidence: 95%
- Description and treatment information
- Mock audio playback simulation

## 🎨 UI/UX Features

### Material Design 3
- Green color scheme (crop/agriculture theme)
- Elevated cards for content sections
- Rounded corners and shadows
- Material buttons with icons

### Language Support
1. English
2. हिंदी (Hindi)
3. मराठी (Marathi)
4. தமிழ் (Tamil)
5. తెలుగు (Telugu)
6. ગુજરાતી (Gujarati)
7. ਪੰਜਾਬੀ (Punjabi)
8. বাংলা (Bengali)

### Navigation Flow
```
CameraFragment → (capture & upload) → ResultsFragment → (back) → CameraFragment
```

## 🧪 Testing

### Manual Testing Checklist

- [ ] Camera permission request
- [ ] Camera preview displays correctly
- [ ] Image capture works
- [ ] Upload to backend (or mock data)
- [ ] Results display correctly
- [ ] Language selector works
- [ ] Audio playback (if backend available)
- [ ] Back navigation works
- [ ] App handles network errors gracefully

### Test on Multiple Devices
- Different screen sizes
- Different Android versions (7.0+)
- Emulator and physical devices

## 🐛 Troubleshooting

### Camera not working
- Check camera permissions in Settings
- Ensure device has a camera
- Try restarting the app

### API connection failed
- Verify backend server is running
- Check BASE_URL in ApiClient.java
- For real device, ensure same WiFi network
- Check firewall settings

### Build errors
- Clean and rebuild: `./gradlew clean build`
- Invalidate caches in Android Studio
- Update Gradle and dependencies

## 📝 Development Notes

### Code Style
- Java naming conventions
- Proper null checks
- Error handling with try-catch
- Logging with Log.e/d/i

### Best Practices
- Fragment lifecycle awareness
- Resource cleanup (camera, media player)
- Async operations on background threads
- UI updates on main thread

## 🚀 Future Enhancements

- [ ] Image gallery selection
- [ ] History of past detections
- [ ] Offline mode with cached results
- [ ] Share results feature
- [ ] Dark mode support
- [ ] Crop type selection
- [ ] Multiple image upload
- [ ] Real-time detection

## 👥 Developer

**Sohan** - Mobile App Development (Native Android Java)

## 📄 License

This project is part of academic coursework.

---

**Happy Coding! 🌱📱**
