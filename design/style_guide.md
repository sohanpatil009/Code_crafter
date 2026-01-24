# 🎨 Crop Disease Detection - Design System & Style Guide

## 🌈 Color Palette

### Primary Colors
```
Primary Green:    #4CAF50  (Agriculture/Growth theme)
Primary Dark:     #388E3C  (Darker shade for emphasis)
Primary Light:    #C8E6C9  (Light backgrounds)
```

### Secondary Colors
```
Secondary Green:  #81C784  (Light accent color)
Accent Teal:      #26A69A  (Interactive elements)
Success Green:    #66BB6A  (Success states)
```

### Status Colors
```
Warning Orange:   #FF9800  (Disease alerts)
Warning Light:    #FFE0B2  (Warning backgrounds)
Error Red:        #F44336  (Critical issues)
Error Light:      #FFCDD2  (Error backgrounds)
Info Blue:        #2196F3  (Information)
Info Light:       #BBDEFB  (Info backgrounds)
```

### Neutral Colors
```
Background:       #F5F5F5  (Main background)
Surface:          #FFFFFF  (Card backgrounds)
Surface Variant:  #F8F9FA  (Alternate surfaces)
Outline:          #E0E0E0  (Borders and dividers)
```

### Text Colors
```
Text Primary:     #212121  (Main text)
Text Secondary:   #757575  (Secondary text)
Text Disabled:    #BDBDBD  (Disabled text)
Text On Primary:  #FFFFFF  (Text on primary color)
```

## 🔤 Typography

### Font Family
- **Primary**: Roboto (Android default)
- **Fallback**: Sans-serif system fonts

### Text Styles

#### Headlines
```
H1 - App Title:       32sp, Bold, #212121
H2 - Screen Title:    24sp, Medium, #212121
H3 - Section Header:  20sp, Medium, #212121
H4 - Card Title:      18sp, Medium, #212121
```

#### Body Text
```
Body Large:           16sp, Regular, #212121
Body Medium:          14sp, Regular, #212121
Body Small:           12sp, Regular, #757575
```

#### Labels & Buttons
```
Button Text:          14sp, Medium, #FFFFFF
Label Large:          14sp, Medium, #212121
Label Small:          12sp, Medium, #757575
Caption:              10sp, Regular, #757575
```

## 📐 Spacing & Layout

### Grid System
- **Base Unit**: 8dp
- **Margins**: 16dp (2 units)
- **Padding**: 8dp, 16dp, 24dp
- **Component Spacing**: 8dp, 16dp, 24dp, 32dp

### Screen Margins
```
Horizontal Margin:    16dp
Vertical Margin:      16dp
Content Padding:      16dp
Card Padding:         16dp
```

### Component Spacing
```
Small Gap:            8dp
Medium Gap:           16dp
Large Gap:            24dp
Section Gap:          32dp
```

## 🎯 Component Styles

### Buttons

#### Primary Button
```
Background:           #4CAF50
Text Color:           #FFFFFF
Corner Radius:        8dp
Height:               48dp
Padding:              16dp horizontal
Elevation:            2dp
```

#### Secondary Button
```
Background:           Transparent
Border:               2dp solid #4CAF50
Text Color:           #4CAF50
Corner Radius:        8dp
Height:               48dp
Padding:              16dp horizontal
```

#### Floating Action Button (FAB)
```
Background:           #4CAF50
Icon Color:           #FFFFFF
Size:                 56dp
Corner Radius:        28dp (circular)
Elevation:            6dp
```

### Cards

#### Disease Result Card
```
Background:           #FFFFFF
Corner Radius:        12dp
Elevation:            4dp
Padding:              16dp
Margin:               8dp horizontal, 4dp vertical
Border:               None
```

#### Info Card
```
Background:           #F8F9FA
Corner Radius:        8dp
Elevation:            2dp
Padding:              12dp
Border:               1dp solid #E0E0E0
```

### Input Fields

#### Text Input
```
Background:           #F5F5F5
Border:               1dp solid #E0E0E0
Corner Radius:        8dp
Height:               48dp
Padding:              12dp horizontal
Text Size:            16sp
```

#### Focused State
```
Border Color:         #4CAF50
Border Width:         2dp
```

### Audio Player Controls

#### Play Button
```
Background:           #4CAF50
Icon Color:           #FFFFFF
Size:                 64dp
Corner Radius:        32dp (circular)
Elevation:            4dp
```

#### Control Buttons (Pause, Stop)
```
Background:           #81C784
Icon Color:           #FFFFFF
Size:                 48dp
Corner Radius:        24dp (circular)
Elevation:            2dp
```

#### Progress Bar
```
Track Color:          #E0E0E0
Progress Color:       #4CAF50
Height:               4dp
Corner Radius:        2dp
```

### Language Selector

#### Language Chip
```
Background:           #F5F5F5
Selected Background:  #4CAF50
Text Color:           #212121
Selected Text:        #FFFFFF
Corner Radius:        16dp
Padding:              8dp horizontal, 4dp vertical
Height:               32dp
```

## 🖼️ Iconography

### Icon Style
- **Style**: Material Design Icons
- **Weight**: Regular (400)
- **Size**: 24dp (standard), 32dp (large), 16dp (small)
- **Color**: #757575 (default), #4CAF50 (active)

### Key Icons
```
Camera:               camera_alt
Microphone:           mic
Play:                 play_arrow
Pause:                pause
Stop:                 stop
Language:             language
History:              history
Info:                 info
Warning:              warning
Error:                error
Success:              check_circle
```

## 📱 Screen Layouts

### Camera Screen
```
- Full-screen camera preview
- Floating capture button (bottom center)
- Language selector (top right)
- Back button (top left)
```

### Results Screen
```
- Disease image (top)
- Disease name and confidence (below image)
- Audio controls (center)
- Disease information card (bottom)
- Action buttons (bottom)
```

### Language Selector
```
- Grid layout (2 columns)
- Language chips with flags
- Current selection highlighted
- Apply button (bottom)
```

## 🎵 Audio Player Design

### Player Layout
```
┌─────────────────────────────────────┐
│  🔊 Disease Information Audio       │
├─────────────────────────────────────┤
│     ⏮️  ⏯️  ⏭️     🔊  ⬇️         │
│                                     │
│  ████████████░░░░░░░░  2:34 / 4:12  │
├─────────────────────────────────────┤
│  🌐 Language: हिंदी (Hindi)         │
└─────────────────────────────────────┘
```

### Audio Controls
- **Play/Pause**: Large circular button (64dp)
- **Stop**: Medium button (48dp)
- **Volume**: Slider with icon
- **Download**: Icon button
- **Progress**: Horizontal progress bar
- **Time**: Current/Total duration

## 🌐 Multi-Language Support

### Language Display
```
Hindi:     हिंदी
English:   English
Marathi:   मराठी
Tamil:     தமிழ்
Telugu:    తెలుగు
Gujarati:  ગુજરાતી
Punjabi:   ਪੰਜਾਬੀ
Bengali:   বাংলা
```

### Language Selector Design
- Flag icons for each language
- Native script display
- English name as subtitle
- Radio button selection
- Smooth transitions

## ♿ Accessibility Guidelines

### Color Contrast
- **Minimum Ratio**: 4.5:1 for normal text
- **Large Text**: 3:1 for 18sp+ or 14sp+ bold
- **Interactive Elements**: 3:1 minimum

### Touch Targets
- **Minimum Size**: 48dp x 48dp
- **Recommended**: 56dp x 56dp for primary actions
- **Spacing**: 8dp minimum between targets

### Text Accessibility
- **Font Size**: Minimum 12sp, recommended 14sp+
- **Line Height**: 1.4x font size minimum
- **Text Scaling**: Support up to 200% scaling

### Audio Accessibility
- **Visual Indicators**: Progress bars, play states
- **Alternative Text**: Descriptions for all audio content
- **Captions**: Text alternatives for audio information

## 📐 Responsive Design

### Screen Sizes
```
Small Phone:    320dp - 480dp width
Medium Phone:   480dp - 600dp width
Large Phone:    600dp - 720dp width
Tablet:         720dp+ width
```

### Breakpoints
- **Compact**: < 600dp (single column)
- **Medium**: 600dp - 840dp (flexible layout)
- **Expanded**: > 840dp (multi-column)

## 🎨 Visual Hierarchy

### Priority Levels
1. **Primary**: Disease name, confidence score
2. **Secondary**: Audio controls, action buttons
3. **Tertiary**: Additional information, metadata
4. **Supporting**: Labels, captions, timestamps

### Emphasis Techniques
- **Color**: Primary green for important elements
- **Size**: Larger text for key information
- **Weight**: Bold for emphasis
- **Position**: Top/center for priority content
- **Contrast**: High contrast for readability

## 🔄 Animation & Transitions

### Transition Duration
```
Fast:           150ms (micro-interactions)
Standard:       300ms (screen transitions)
Slow:           500ms (complex animations)
```

### Easing Curves
```
Standard:       cubic-bezier(0.4, 0.0, 0.2, 1)
Decelerate:     cubic-bezier(0.0, 0.0, 0.2, 1)
Accelerate:     cubic-bezier(0.4, 0.0, 1, 1)
```

### Animation Types
- **Fade**: Opacity transitions
- **Slide**: Position transitions
- **Scale**: Size transitions
- **Ripple**: Touch feedback

## 📋 Design Checklist

### Visual Design
- [ ] Color palette applied consistently
- [ ] Typography hierarchy established
- [ ] Spacing system implemented
- [ ] Component styles defined
- [ ] Icons selected and sized
- [ ] Images optimized

### Interaction Design
- [ ] Touch targets sized appropriately
- [ ] Feedback provided for all interactions
- [ ] Loading states designed
- [ ] Error states handled
- [ ] Success states celebrated

### Accessibility
- [ ] Color contrast verified
- [ ] Text scaling supported
- [ ] Alternative text provided
- [ ] Keyboard navigation possible
- [ ] Screen reader compatible

### Multi-Language
- [ ] Text expansion accommodated
- [ ] RTL languages considered
- [ ] Font support verified
- [ ] Cultural sensitivity reviewed

---

**Created by:** Shravani (UI/UX Designer)
**Last Updated:** January 24, 2026
**Version:** 1.0