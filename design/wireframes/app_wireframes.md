# 📱 Mobile App Wireframes - Crop Disease Detection

## 🎯 App Flow Overview

```
Splash Screen → Camera Screen → Results Screen → Audio Player → History
      ↓              ↓              ↓              ↓           ↓
Language Setup → Language Select → Language Select → Settings → Help
```

## 📱 Screen Wireframes

### 1. Splash Screen
```
┌─────────────────────────────────────┐
│                                     │
│              🌱 LOGO                │
│                                     │
│        Crop Disease Detection       │
│                                     │
│            Loading...               │
│         ████████████░░░             │
│                                     │
│                                     │
│         Powered by AI 🤖            │
│                                     │
└─────────────────────────────────────┘
```

### 2. Language Selection Screen (First Time)
```
┌─────────────────────────────────────┐
│  ← Back          Choose Language    │
├─────────────────────────────────────┤
│                                     │
│  Select your preferred language:    │
│                                     │
│  ┌─────────────┐ ┌─────────────┐   │
│  │ 🇮🇳 हिंदी    │ │ 🇬🇧 English  │   │
│  │   Hindi     │ │             │   │
│  └─────────────┘ └─────────────┘   │
│                                     │
│  ┌─────────────┐ ┌─────────────┐   │
│  │ 🇮🇳 मराठी    │ │ 🇮🇳 தமிழ்     │   │
│  │  Marathi    │ │   Tamil     │   │
│  └─────────────┘ └─────────────┘   │
│                                     │
│  ┌─────────────┐ ┌─────────────┐   │
│  │ 🇮🇳 తెలుగు    │ │ 🇮🇳 ગુજરાતી   │   │
│  │  Telugu     │ │  Gujarati   │   │
│  └─────────────┘ └─────────────┘   │
│                                     │
│  ┌─────────────┐ ┌─────────────┐   │
│  │ 🇮🇳 ਪੰਜਾਬੀ    │ │ 🇮🇳 বাংলা     │   │
│  │  Punjabi    │ │  Bengali    │   │
│  └─────────────┘ └─────────────┘   │
│                                     │
│         ┌─────────────┐             │
│         │   Continue  │             │
│         └─────────────┘             │
└─────────────────────────────────────┘
```

### 3. Camera Screen (Main Screen)
```
┌─────────────────────────────────────┐
│  ← Back    📷 Camera      🌐 हिंदी   │
├─────────────────────────────────────┤
│                                     │
│                                     │
│         CAMERA PREVIEW              │
│                                     │
│         [Live camera feed           │
│          showing crop/leaf          │
│          with focus guides]         │
│                                     │
│                                     │
│                                     │
│                                     │
│  📁 Gallery              📷         │
│                                     │
│                      ┌─────────┐   │
│                      │    📷    │   │
│                      │ Capture │   │
│                      └─────────┘   │
│                                     │
│  💡 Tips: Point camera at leaf     │
└─────────────────────────────────────┘
```

### 4. Processing Screen
```
┌─────────────────────────────────────┐
│  ← Back      Processing...          │
├─────────────────────────────────────┤
│                                     │
│         ┌─────────────────┐         │
│         │                 │         │
│         │   [Captured     │         │
│         │    Image]       │         │
│         │                 │         │
│         └─────────────────┘         │
│                                     │
│              🔄 Analyzing...        │
│                                     │
│         ████████████░░░░░░          │
│              75% Complete           │
│                                     │
│    🤖 AI is detecting diseases...   │
│                                     │
│         Please wait a moment        │
│                                     │
└─────────────────────────────────────┘
```

### 5. Results Screen
```
┌─────────────────────────────────────┐
│  ← Back      Disease Detected   ⋮   │
├─────────────────────────────────────┤
│         ┌─────────────────┐         │
│         │                 │         │
│         │   [Disease      │         │
│         │    Image]       │         │
│         │                 │         │
│         └─────────────────┘         │
│                                     │
│  🦠 Tomato Early Blight             │
│  📊 Confidence: 87%                 │
│                                     │
│  ┌─────────────────────────────────┐ │
│  │ 🔊 Audio Information            │ │
│  │                                 │ │
│  │  ⏮️  ⏯️  ⏭️     🔊  ⬇️         │ │
│  │                                 │ │
│  │ ████████████░░░░░░░░  2:34/4:12 │ │
│  │                                 │ │
│  │ 🌐 Language: हिंदी (Hindi)       │ │
│  └─────────────────────────────────┘ │
│                                     │
│  📋 Disease Information:            │
│  • Symptoms: Brown spots on leaves  │
│  • Treatment: Apply fungicide       │
│  • Prevention: Proper spacing       │
│                                     │
│  ┌─────────────┐ ┌─────────────┐   │
│  │   📤 Share  │ │  💾 Save    │   │
│  └─────────────┘ └─────────────┘   │
└─────────────────────────────────────┘
```

### 6. Audio Player (Expanded)
```
┌─────────────────────────────────────┐
│  ← Back      Audio Player       ⋮   │
├─────────────────────────────────────┤
│                                     │
│  🔊 Disease Information Audio       │
│                                     │
│         ┌─────────────────┐         │
│         │                 │         │
│         │   [Waveform     │         │
│         │   Animation]    │         │
│         │                 │         │
│         └─────────────────┘         │
│                                     │
│      ⏮️      ⏯️      ⏭️             │
│   Previous  Play   Next             │
│                                     │
│  ████████████████░░░░░░░░░░         │
│           2:34 / 4:12               │
│                                     │
│  🔊 ████████░░ Volume: 80%          │
│                                     │
│  🌐 Language: हिंदी (Hindi)         │
│                                     │
│  ⚡ Speed: 1.0x  📥 Download        │
│                                     │
│  ┌─────────────────────────────────┐ │
│  │ Now Playing:                    │ │
│  │ "टमाटर में अर्ली ब्लाइट रोग..."   │ │
│  └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

### 7. History Screen
```
┌─────────────────────────────────────┐
│  ← Back        History          🔍  │
├─────────────────────────────────────┤
│                                     │
│  📅 Recent Detections               │
│                                     │
│  ┌─────────────────────────────────┐ │
│  │ 📷 [img] Tomato Early Blight    │ │
│  │ 📊 87% • 2 hours ago           │ │
│  │ 🔊 ⏯️                          │ │
│  └─────────────────────────────────┘ │
│                                     │
│  ┌─────────────────────────────────┐ │
│  │ 📷 [img] Potato Late Blight     │ │
│  │ 📊 92% • Yesterday              │ │
│  │ 🔊 ⏯️                          │ │
│  └─────────────────────────────────┘ │
│                                     │
│  ┌─────────────────────────────────┐ │
│  │ 📷 [img] Corn Common Rust       │ │
│  │ 📊 78% • 3 days ago            │ │
│  │ 🔊 ⏯️                          │ │
│  └─────────────────────────────────┘ │
│                                     │
│  ┌─────────────────────────────────┐ │
│  │ 📷 [img] Apple Scab              │ │
│  │ 📊 85% • 1 week ago            │ │
│  │ 🔊 ⏯️                          │ │
│  └─────────────────────────────────┘ │
│                                     │
│         Load More...                │
└─────────────────────────────────────┘
```

### 8. Settings Screen
```
┌─────────────────────────────────────┐
│  ← Back        Settings             │
├─────────────────────────────────────┤
│                                     │
│  🌐 Language & Region               │
│  ┌─────────────────────────────────┐ │
│  │ App Language: हिंदी (Hindi)     │ │
│  │ Audio Language: हिंदी (Hindi)   │ │
│  └─────────────────────────────────┘ │
│                                     │
│  🔊 Audio Settings                  │
│  ┌─────────────────────────────────┐ │
│  │ Volume: ████████░░ 80%          │ │
│  │ Speed: 1.0x                     │ │
│  │ Auto-play: ON                   │ │
│  └─────────────────────────────────┘ │
│                                     │
│  📱 App Preferences                 │
│  ┌─────────────────────────────────┐ │
│  │ Save Images: ON                 │ │
│  │ Show Confidence: ON             │ │
│  │ Dark Mode: OFF                  │ │
│  └─────────────────────────────────┘ │
│                                     │
│  📋 About                           │
│  ┌─────────────────────────────────┐ │
│  │ Version: 1.0.0                  │ │
│  │ Privacy Policy                  │ │
│  │ Terms of Service                │ │
│  └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

### 9. Help Screen
```
┌─────────────────────────────────────┐
│  ← Back         Help            🔍  │
├─────────────────────────────────────┤
│                                     │
│  ❓ Frequently Asked Questions      │
│                                     │
│  ┌─────────────────────────────────┐ │
│  │ ▶ How to take a good photo?     │ │
│  └─────────────────────────────────┘ │
│                                     │
│  ┌─────────────────────────────────┐ │
│  │ ▶ What diseases can be detected?│ │
│  └─────────────────────────────────┘ │
│                                     │
│  ┌─────────────────────────────────┐ │
│  │ ▶ How accurate are predictions? │ │
│  └─────────────────────────────────┘ │
│                                     │
│  ┌─────────────────────────────────┐ │
│  │ ▶ How to use audio features?    │ │
│  └─────────────────────────────────┘ │
│                                     │
│  📖 User Guide                      │
│  ┌─────────────────────────────────┐ │
│  │ 📷 Taking Photos                │ │
│  │ 🔊 Using Audio                  │ │
│  │ 🌐 Changing Language            │ │
│  │ 📋 Understanding Results        │ │
│  └─────────────────────────────────┘ │
│                                     │
│  📞 Contact Support                 │
│  ┌─────────────────────────────────┐ │
│  │ 📧 Email: support@cropai.com    │ │
│  │ 📱 WhatsApp: +91-XXXX-XXXX     │ │
│  └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

## 🔄 User Flow Diagrams

### Primary User Journey
```
Start App → Select Language → Camera Screen → Capture Photo → 
Processing → View Results → Listen to Audio → Save/Share → 
View History → Settings/Help
```

### Audio Feature Flow
```
Results Screen → Tap Audio Button → Audio Player Opens → 
Select Language → Play Audio → Control Playback → 
Download Audio → Return to Results
```

### Language Change Flow
```
Any Screen → Settings → Language Settings → Select New Language → 
Confirm Change → App Restarts → New Language Applied
```

## 📱 Component Wireframes

### Disease Result Card
```
┌─────────────────────────────────────┐
│ ┌─────┐ Tomato Early Blight         │
│ │ IMG │ Confidence: 87%             │
│ └─────┘ 🔊 ⏯️  📤  💾             │
└─────────────────────────────────────┘
```

### Audio Control Bar
```
┌─────────────────────────────────────┐
│  ⏮️  ⏯️  ⏭️     🔊  ⬇️             │
│ ████████████░░░░░░░░  2:34 / 4:12   │
│ 🌐 हिंदी (Hindi)                    │
└─────────────────────────────────────┘
```

### Language Selector Chip
```
┌─────────────┐
│ 🇮🇳 हिंदी    │ ← Selected (Green)
│   Hindi     │
└─────────────┘

┌─────────────┐
│ 🇬🇧 English  │ ← Unselected (Gray)
│             │
└─────────────┘
```

## 📐 Layout Specifications

### Screen Dimensions
- **Width**: 360dp (standard Android)
- **Height**: 640dp (standard Android)
- **Safe Area**: Account for status bar and navigation

### Grid System
- **Columns**: 4 columns for mobile
- **Gutter**: 16dp between columns
- **Margin**: 16dp from screen edges

### Component Sizes
- **Header Height**: 56dp
- **Button Height**: 48dp
- **Card Height**: Variable (min 72dp)
- **List Item**: 72dp
- **FAB Size**: 56dp

## 🎯 Interaction States

### Button States
```
Default:    Background #4CAF50, Text #FFFFFF
Pressed:    Background #388E3C, Text #FFFFFF
Disabled:   Background #E0E0E0, Text #BDBDBD
Loading:    Background #4CAF50, Spinner #FFFFFF
```

### Card States
```
Default:    Elevation 2dp, Background #FFFFFF
Hover:      Elevation 4dp, Background #FFFFFF
Pressed:    Elevation 1dp, Background #F5F5F5
Selected:   Border 2dp #4CAF50, Background #FFFFFF
```

## 📱 Responsive Behavior

### Small Screens (< 360dp)
- Reduce padding to 12dp
- Stack buttons vertically
- Smaller text sizes
- Compact audio controls

### Large Screens (> 480dp)
- Increase padding to 24dp
- Side-by-side layouts
- Larger touch targets
- Expanded audio player

### Tablet Screens (> 600dp)
- Two-column layouts
- Master-detail views
- Larger images
- Extended information panels

---

**Created by:** Shravani (UI/UX Designer)
**Purpose:** Mobile app wireframes and user flow documentation
**Last Updated:** January 24, 2026