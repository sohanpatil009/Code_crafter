# ♿ Accessibility Guidelines - Crop Disease Detection App

## 🎯 Accessibility Mission

**Goal**: Make crop disease detection accessible to all farmers, regardless of their physical abilities, technical skills, or literacy levels.

**Commitment**: Follow WCAG 2.1 AA standards and Android accessibility best practices to ensure inclusive design.

## 🌟 Accessibility Principles

### 1. Perceivable
- Information must be presentable in ways users can perceive
- Provide text alternatives for images
- Offer captions and audio descriptions
- Ensure sufficient color contrast

### 2. Operable
- Interface components must be operable by all users
- Make all functionality keyboard accessible
- Give users enough time to read content
- Don't use content that causes seizures

### 3. Understandable
- Information and UI operation must be understandable
- Make text readable and understandable
- Make content appear and operate predictably
- Help users avoid and correct mistakes

### 4. Robust
- Content must be robust enough for various assistive technologies
- Maximize compatibility with assistive technologies
- Use valid, semantic code
- Ensure forward compatibility

## 👥 Target Accessibility Users

### Visual Impairments
- **Blind users**: Complete reliance on screen readers
- **Low vision users**: Need high contrast and magnification
- **Color blind users**: Cannot distinguish certain colors
- **Light sensitivity**: Need dark mode options

### Hearing Impairments
- **Deaf users**: Cannot hear audio content
- **Hard of hearing**: Need volume control and captions
- **Audio processing issues**: Need visual alternatives

### Motor Impairments
- **Limited dexterity**: Difficulty with precise touch
- **Tremors**: Need larger touch targets
- **One-handed use**: Need alternative interaction methods
- **Voice control**: Prefer speech input

### Cognitive Impairments
- **Learning disabilities**: Need simple, clear instructions
- **Memory issues**: Need consistent navigation
- **Attention disorders**: Need focused, distraction-free design
- **Language barriers**: Need visual cues and simple language

## 📱 Screen Reader Support

### TalkBack Integration (Android)

#### Content Descriptions
```xml
<!-- Camera capture button -->
<Button
    android:contentDescription="Capture photo of plant leaf"
    android:text="📷 Capture" />

<!-- Disease result -->
<TextView
    android:contentDescription="Disease detected: Tomato Early Blight with 87 percent confidence"
    android:text="🦠 Tomato Early Blight - 87%" />

<!-- Audio play button -->
<Button
    android:contentDescription="Play audio explanation in Hindi"
    android:text="▶️ Play Audio" />
```

#### Heading Structure
```
H1: App Title - "Crop Disease Detection"
H2: Screen Titles - "Camera", "Results", "History"
H3: Section Headers - "Disease Information", "Treatment Advice"
H4: Subsections - "Symptoms", "Prevention"
```

#### Reading Order
1. **Screen title** (H2)
2. **Main content** (disease image, name, confidence)
3. **Action buttons** (audio, save, share)
4. **Additional information** (symptoms, treatment)
5. **Navigation options** (back, menu)

### Screen Reader Announcements
```
Camera Screen:
"Camera screen. Point camera at plant leaf and tap capture button to detect diseases."

Results Screen:
"Results screen. Disease detected: Tomato Early Blight with 87 percent confidence. Tap play button to hear treatment advice."

Audio Player:
"Audio player. Now playing disease information in Hindi. Use play, pause, and stop buttons to control playback."
```

## 🎨 Visual Accessibility

### Color Contrast Requirements

#### Text Contrast Ratios
```
Normal Text (14sp+):     4.5:1 minimum
Large Text (18sp+):      3.0:1 minimum
Interactive Elements:    3.0:1 minimum
Graphical Objects:       3.0:1 minimum
```

#### Color Combinations
```
✅ Good Contrast:
- Black text (#000000) on white background (#FFFFFF) = 21:1
- Dark gray text (#212121) on white background = 16.7:1
- White text (#FFFFFF) on green background (#4CAF50) = 4.5:1

❌ Poor Contrast:
- Light gray text (#BDBDBD) on white background = 1.9:1
- Yellow text (#FFEB3B) on white background = 1.1:1
- Green text (#4CAF50) on white background = 3.4:1 (below 4.5:1)
```

### Color Independence
- **Never rely solely on color** to convey information
- **Use icons + color** for status indicators
- **Provide text labels** for color-coded elements
- **Test with color blindness simulators**

#### Status Indicators
```
✅ Good:
Success: ✅ Green checkmark + "Success" text
Warning: ⚠️ Orange triangle + "Warning" text
Error: ❌ Red X + "Error" text

❌ Bad:
Success: Green background only
Warning: Orange background only
Error: Red background only
```

### Text Scaling Support
```
Font Scaling Levels:
- Small: 0.85x (12sp → 10sp)
- Default: 1.0x (14sp → 14sp)
- Large: 1.15x (14sp → 16sp)
- Extra Large: 1.3x (14sp → 18sp)
- Huge: 2.0x (14sp → 28sp)
```

#### Responsive Text Layout
```
Default Layout (14sp):
┌─────────────────────────────────────┐
│ 🦠 Tomato Early Blight             │
│ 📊 Confidence: 87%                 │
│ ┌─────────────┐ ┌─────────────┐   │
│ │  🔊 Audio   │ │  💾 Save    │   │
│ └─────────────┘ └─────────────┘   │
└─────────────────────────────────────┘

Large Text Layout (28sp):
┌─────────────────────────────────────┐
│ 🦠 Tomato Early                     │
│    Blight                           │
│                                     │
│ 📊 Confidence:                      │
│    87%                              │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │        🔊 Audio                 │ │
│ └─────────────────────────────────┘ │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │        💾 Save                  │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

## 🔊 Audio Accessibility

### Audio Alternatives for Visual Content

#### Image Descriptions
```
Disease Image Alt Text:
"Close-up photograph of a tomato leaf showing brown circular spots with yellow halos, characteristic of early blight disease. The spots are scattered across the leaf surface with some showing concentric rings."

Camera Preview Alt Text:
"Live camera preview showing plant leaf positioned in center frame with focus guides visible. Tap capture button to take photo."
```

#### Audio Descriptions for Visual Elements
```
Results Screen Audio Description:
"Results screen displaying a photograph of the analyzed leaf at the top. Below the image, the disease name 'Tomato Early Blight' is shown in large text with a confidence score of 87 percent. Audio playback controls are centered below with play, pause, and stop buttons. Treatment information is displayed at the bottom."
```

### TTS Enhancements

#### Speech Rate Control
```
Slow: 0.5x speed (120 words per minute)
Normal: 1.0x speed (180 words per minute)
Fast: 1.5x speed (240 words per minute)
Very Fast: 2.0x speed (300 words per minute)
```

#### Voice Customization
```
Hindi Voice Options:
- Male voice (default)
- Female voice (alternative)
- Regional accent variations

Volume Control:
- Quiet: 30%
- Normal: 70%
- Loud: 100%
```

#### Audio Content Structure
```
1. Disease Name: "टमाटर में अर्ली ब्लाइट रोग पाया गया है"
2. Confidence: "इस निदान की सटीकता 87 प्रतिशत है"
3. Symptoms: "लक्षण: पत्तियों पर भूरे धब्बे दिखाई देते हैं"
4. Treatment: "उपचार: फंगीसाइड का छिड़काव करें"
5. Prevention: "बचाव: पौधों के बीच उचित दूरी रखें"
```

## 👆 Touch Accessibility

### Touch Target Sizes
```
Minimum Size: 48dp x 48dp (Android guideline)
Recommended: 56dp x 56dp (comfortable tapping)
Large Targets: 64dp x 64dp (primary actions)
```

#### Button Sizing Examples
```
Primary Action (Capture):
┌─────────────────┐
│                 │ 64dp
│   📷 Capture    │
│                 │
└─────────────────┘
     120dp

Secondary Action (Save):
┌─────────────┐
│             │ 48dp
│  💾 Save    │
│             │
└─────────────┘
    80dp

Icon Button (Menu):
┌─────────┐
│         │ 48dp
│   ⋮     │
│         │
└─────────┘
   48dp
```

### Touch Target Spacing
```
Minimum Spacing: 8dp between targets
Recommended: 16dp between targets
Large Spacing: 24dp for critical actions
```

### Alternative Input Methods

#### Voice Commands
```
"Take photo" → Captures image
"Play audio" → Starts TTS playback
"Stop audio" → Stops TTS playback
"Go back" → Returns to previous screen
"Open settings" → Opens settings menu
"Change language" → Opens language selector
```

#### Gesture Alternatives
```
Swipe Right: Next item in list
Swipe Left: Previous item in list
Double Tap: Activate button/link
Long Press: Show context menu
Pinch: Zoom in/out (for images)
```

## 🧠 Cognitive Accessibility

### Simple Language Guidelines

#### Writing Principles
- **Use common words** instead of technical terms
- **Keep sentences short** (max 20 words)
- **Use active voice** instead of passive
- **Provide examples** for complex concepts
- **Use bullet points** for lists

#### Technical Term Simplification
```
Instead of: "Phytophthora infestans pathogen"
Use: "Late blight disease"

Instead of: "Fungicidal application recommended"
Use: "Spray fungicide medicine"

Instead of: "Implement prophylactic measures"
Use: "Take steps to prevent disease"
```

### Clear Instructions

#### Step-by-Step Guidance
```
Camera Instructions:
1. 📱 Hold phone steady
2. 🍃 Point at diseased leaf
3. 📷 Tap capture button
4. ⏳ Wait for results

Audio Instructions:
1. 🔊 Tap play button
2. 👂 Listen to advice
3. ⏸️ Tap pause if needed
4. 💾 Save for later
```

### Error Prevention & Recovery

#### Input Validation
```
Photo Quality Check:
❌ "Image too blurry - please retake"
❌ "Image too dark - use better lighting"
❌ "No leaf detected - point at plant leaf"
✅ "Good image quality - processing..."
```

#### Error Messages
```
Instead of: "Network error 404"
Use: "Cannot connect to internet. Please check your connection and try again."

Instead of: "Invalid file format"
Use: "This image type is not supported. Please use JPG or PNG format."
```

## 📱 Platform-Specific Accessibility

### Android Accessibility Services

#### TalkBack Integration
```xml
<!-- Enable TalkBack focus -->
<View android:focusable="true" />

<!-- Custom TalkBack actions -->
<View android:accessibilityActions="click,long_click" />

<!-- Live regions for dynamic content -->
<View android:accessibilityLiveRegion="polite" />
```

#### Switch Access Support
```xml
<!-- Enable switch navigation -->
<View android:focusable="true"
      android:clickable="true" />

<!-- Group related elements -->
<LinearLayout android:screenReaderFocusable="true">
    <!-- Child elements -->
</LinearLayout>
```

### Accessibility Settings Integration

#### System Settings Respect
```
Text Size: Follow system text scaling
High Contrast: Respect system high contrast mode
Animation: Respect reduced motion preferences
Sound: Follow system sound settings
```

## 🧪 Accessibility Testing

### Automated Testing Tools

#### Android Accessibility Scanner
```
Tests to Run:
- Content labeling
- Touch target size
- Color contrast
- Text scaling
- Focus management
```

#### Manual Testing Checklist

##### Screen Reader Testing
- [ ] All images have meaningful alt text
- [ ] All buttons have descriptive labels
- [ ] Heading structure is logical
- [ ] Reading order makes sense
- [ ] Dynamic content is announced

##### Keyboard Navigation
- [ ] All interactive elements are focusable
- [ ] Focus order is logical
- [ ] Focus indicators are visible
- [ ] No keyboard traps exist
- [ ] Shortcuts work as expected

##### Visual Testing
- [ ] Text contrast meets WCAG standards
- [ ] Color is not the only information method
- [ ] Text scales up to 200% without issues
- [ ] UI remains usable in high contrast mode
- [ ] All text is readable

##### Motor Testing
- [ ] Touch targets are at least 48dp
- [ ] Adequate spacing between targets
- [ ] Alternative input methods work
- [ ] Gestures have alternatives
- [ ] Voice commands function properly

### User Testing with Disabilities

#### Participant Recruitment
- **Visual impairments**: 2 blind users, 2 low vision users
- **Hearing impairments**: 2 deaf users, 1 hard of hearing user
- **Motor impairments**: 2 users with limited dexterity
- **Cognitive impairments**: 2 users with learning disabilities

#### Testing Scenarios
1. **Complete disease detection workflow** using assistive technology
2. **Navigate app using only keyboard/switch access**
3. **Use app with screen reader** and provide feedback
4. **Test with maximum text scaling** enabled
5. **Use voice commands** for all interactions

## 📋 Accessibility Implementation Checklist

### Design Phase
- [ ] Color contrast ratios calculated and verified
- [ ] Touch targets sized appropriately
- [ ] Alternative text planned for all images
- [ ] Heading structure designed
- [ ] Focus order planned

### Development Phase
- [ ] Content descriptions added to all UI elements
- [ ] Semantic markup used correctly
- [ ] Keyboard navigation implemented
- [ ] Screen reader testing completed
- [ ] Accessibility services integrated

### Testing Phase
- [ ] Automated accessibility tests run
- [ ] Manual testing with assistive technology
- [ ] User testing with disabled participants
- [ ] Performance testing with accessibility features
- [ ] Documentation updated with accessibility features

### Launch Phase
- [ ] Accessibility statement published
- [ ] User guides include accessibility instructions
- [ ] Support channels prepared for accessibility questions
- [ ] Feedback mechanism for accessibility issues
- [ ] Regular accessibility audits scheduled

## 📚 Accessibility Resources

### Guidelines & Standards
- **WCAG 2.1 AA**: Web Content Accessibility Guidelines
- **Android Accessibility**: Google's accessibility guidelines
- **Material Design Accessibility**: Design system accessibility
- **Section 508**: US federal accessibility requirements

### Testing Tools
- **Accessibility Scanner**: Android automated testing
- **TalkBack**: Android screen reader
- **Color Oracle**: Color blindness simulator
- **WAVE**: Web accessibility evaluation tool

### User Communities
- **National Federation of the Blind**: Blind user feedback
- **Hearing Loss Association**: Deaf/HoH user input
- **United Spinal Association**: Motor impairment insights
- **Learning Disabilities Association**: Cognitive accessibility

---

**Created by:** Shravani (UI/UX Designer)
**Purpose:** Comprehensive accessibility guidelines and implementation plan
**Standards:** WCAG 2.1 AA, Android Accessibility Guidelines
**Last Updated:** January 24, 2026