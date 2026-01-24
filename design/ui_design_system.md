# Smart Agriculture App - UI Design System
**Premium Glassmorphism Design for Crop Disease Detection**

## 🎨 Visual Identity

### Color Palette
```css
/* Primary Colors */
--primary-green: #2D5016;      /* Deep forest green */
--primary-olive: #556B2F;      /* Olive drab */
--primary-lime: #9ACD32;       /* Yellow green */
--accent-yellow: #F4E04D;      /* Soft golden yellow */

/* Glassmorphism Colors */
--glass-white: rgba(255, 255, 255, 0.15);
--glass-green: rgba(154, 205, 50, 0.2);
--glass-dark: rgba(45, 80, 22, 0.3);

/* Background Gradients */
--bg-primary: linear-gradient(135deg, #2D5016 0%, #556B2F 100%);
--bg-secondary: linear-gradient(135deg, #9ACD32 0%, #F4E04D 100%);
--bg-glass: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);

/* Text Colors */
--text-primary: #1A1A1A;
--text-secondary: #666666;
--text-light: #FFFFFF;
--text-success: #4CAF50;
--text-warning: #FF9800;
--text-error: #F44336;
```

### Typography
```css
/* Font Family */
font-family: 'Inter', 'SF Pro Display', 'Poppins', system-ui, sans-serif;

/* Font Weights */
--font-light: 300;
--font-regular: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;

/* Font Sizes */
--text-xs: 12px;
--text-sm: 14px;
--text-base: 16px;
--text-lg: 18px;
--text-xl: 20px;
--text-2xl: 24px;
--text-3xl: 30px;
--text-4xl: 36px;
```

### Spacing & Layout
```css
/* Spacing Scale */
--space-xs: 4px;
--space-sm: 8px;
--space-md: 16px;
--space-lg: 24px;
--space-xl: 32px;
--space-2xl: 48px;
--space-3xl: 64px;

/* Border Radius */
--radius-sm: 8px;
--radius-md: 16px;
--radius-lg: 24px;
--radius-xl: 32px;
--radius-full: 9999px;

/* Shadows */
--shadow-sm: 0 2px 8px rgba(45, 80, 22, 0.1);
--shadow-md: 0 4px 16px rgba(45, 80, 22, 0.15);
--shadow-lg: 0 8px 32px rgba(45, 80, 22, 0.2);
--shadow-glow: 0 0 20px rgba(154, 205, 50, 0.3);
```

## 🪟 Glassmorphism Components

### Glass Card Base
```css
.glass-card {
  background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-glow);
}
```

### Floating Action Button
```css
.fab-primary {
  background: linear-gradient(135deg, #9ACD32 0%, #F4E04D 100%);
  border-radius: var(--radius-full);
  box-shadow: var(--shadow-lg);
  border: none;
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.fab-primary:active {
  transform: scale(0.95);
  box-shadow: var(--shadow-glow);
}
```

### Progress Indicators
```css
.progress-ring {
  background: rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-full);
  padding: 4px;
  backdrop-filter: blur(10px);
}

.progress-fill {
  background: linear-gradient(90deg, #9ACD32 0%, #F4E04D 100%);
  border-radius: var(--radius-full);
  height: 8px;
  transition: width 0.5s ease;
}
```

## 📱 Screen Layouts

### 1. Home Dashboard
```
┌─────────────────────────────────────┐
│  🌱 Smart Farm AI        🔔 ⚙️     │
├─────────────────────────────────────┤
│                                     │
│  ╭─────────────────────────────────╮ │
│  │     🌾 Farm Overview           │ │
│  │  ┌─────┐ ┌─────┐ ┌─────┐      │ │
│  │  │ 85% │ │ 12  │ │ 3   │      │ │
│  │  │Hlthy│ │Scnd │ │Alrt │      │ │
│  │  └─────┘ └─────┘ └─────┘      │ │
│  ╰─────────────────────────────────╯ │
│                                     │
│  ╭─────────────────────────────────╮ │
│  │     📊 Recent Scans            │ │
│  │  ┌─────────────────────────┐   │ │
│  │  │ 🍃 Tomato Leaf         │   │ │
│  │  │ ✅ Healthy - 94%       │   │ │
│  │  │ 2 hours ago            │   │ │
│  │  └─────────────────────────┘   │ │
│  ╰─────────────────────────────────╯ │
│                                     │
│  ╭─────────────────────────────────╮ │
│  │     🎯 Quick Actions           │ │
│  │  [📷 Scan] [📈 Reports]       │ │
│  │  [🌡️ Weather] [💡 Tips]       │ │
│  ╰─────────────────────────────────╯ │
│                                     │
├─────────────────────────────────────┤
│  🏠  📷  📊  🌱  👤              │
└─────────────────────────────────────┘
```

### 2. Camera Scan Screen
```
┌─────────────────────────────────────┐
│  ← Scan Crop Disease                │
├─────────────────────────────────────┤
│                                     │
│    ╭─────────────────────────────╮   │
│    │                             │   │
│    │    📷 Camera Preview        │   │
│    │                             │   │
│    │    ┌─────────────────┐      │   │
│    │    │                 │      │   │
│    │    │  Scan Frame     │      │   │
│    │    │                 │      │   │
│    │    └─────────────────┘      │   │
│    │                             │   │
│    ╰─────────────────────────────╯   │
│                                     │
│  ╭─────────────────────────────────╮ │
│  │ 💡 Tips                        │ │
│  │ • Hold steady for 2-3 seconds  │ │
│  │ • Ensure good lighting         │ │
│  │ • Focus on leaf surface        │ │
│  ╰─────────────────────────────────╯ │
│                                     │
│           ┌─────────┐               │
│           │    📷   │               │
│           │ CAPTURE │               │
│           └─────────┘               │
│                                     │
├─────────────────────────────────────┤
│  🏠  📷  📊  🌱  👤              │
└─────────────────────────────────────┘
```

### 3. Analysis Results Screen
```
┌─────────────────────────────────────┐
│  ← Analysis Results                 │
├─────────────────────────────────────┤
│                                     │
│  ╭─────────────────────────────────╮ │
│  │    🍃 Leaf Image Preview       │ │
│  │  ┌─────────────────────────┐   │ │
│  │  │                         │   │ │
│  │  │    Analyzed Image       │   │ │
│  │  │                         │   │ │
│  │  └─────────────────────────┘   │ │
│  ╰─────────────────────────────────╯ │
│                                     │
│  ╭─────────────────────────────────╮ │
│  │    🎯 Detection Results        │ │
│  │                                │ │
│  │  🦠 Early Blight               │ │
│  │  ████████████░░ 87%            │ │
│  │                                │ │
│  │  📊 Confidence Level           │ │
│  │  ████████████████░ 94%         │ │
│  ╰─────────────────────────────────╯ │
│                                     │
│  ╭─────────────────────────────────╮ │
│  │    💡 Recommendations          │ │
│  │  • Apply copper fungicide      │ │
│  │  • Improve air circulation     │ │
│  │  • Monitor weekly              │ │
│  │                                │ │
│  │  [🔊 Listen] [📤 Share]        │ │
│  ╰─────────────────────────────────╯ │
│                                     │
├─────────────────────────────────────┤
│  🏠  📷  📊  🌱  👤              │
└─────────────────────────────────────┘
```

## 🎭 Animation & Interactions

### Micro-interactions
```css
/* Button Press Animation */
@keyframes buttonPress {
  0% { transform: scale(1); }
  50% { transform: scale(0.95); }
  100% { transform: scale(1); }
}

/* Card Hover Effect */
@keyframes cardFloat {
  0% { transform: translateY(0px); }
  100% { transform: translateY(-4px); }
}

/* Progress Animation */
@keyframes progressFill {
  0% { width: 0%; }
  100% { width: var(--progress-width); }
}

/* Scan Animation */
@keyframes scanPulse {
  0% { 
    box-shadow: 0 0 0 0 rgba(154, 205, 50, 0.7);
    transform: scale(1);
  }
  70% { 
    box-shadow: 0 0 0 20px rgba(154, 205, 50, 0);
    transform: scale(1.05);
  }
  100% { 
    box-shadow: 0 0 0 0 rgba(154, 205, 50, 0);
    transform: scale(1);
  }
}
```

### Transition Timing
```css
/* Smooth Transitions */
--transition-fast: 0.15s cubic-bezier(0.4, 0, 0.2, 1);
--transition-normal: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
--transition-slow: 0.5s cubic-bezier(0.4, 0, 0.2, 1);

/* Spring Animation */
--spring: cubic-bezier(0.68, -0.55, 0.265, 1.55);
```

## 📐 Component Specifications

### Navigation Bar
```css
.bottom-nav {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  height: 80px;
  padding: 12px 24px;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 8px 12px;
  border-radius: var(--radius-md);
  transition: var(--transition-normal);
}

.nav-item.active {
  background: rgba(154, 205, 50, 0.2);
  color: var(--primary-lime);
}
```

### Status Cards
```css
.status-card {
  background: var(--glass-white);
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  min-height: 120px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.status-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, #9ACD32 0%, #F4E04D 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--space-md);
}
```

### Scan Frame Overlay
```css
.scan-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 280px;
  height: 280px;
  border: 3px solid rgba(154, 205, 50, 0.8);
  border-radius: var(--radius-xl);
  background: rgba(154, 205, 50, 0.1);
  backdrop-filter: blur(5px);
}

.scan-corners {
  position: absolute;
  width: 40px;
  height: 40px;
  border: 4px solid #9ACD32;
}

.corner-tl { top: -2px; left: -2px; border-right: none; border-bottom: none; }
.corner-tr { top: -2px; right: -2px; border-left: none; border-bottom: none; }
.corner-bl { bottom: -2px; left: -2px; border-right: none; border-top: none; }
.corner-br { bottom: -2px; right: -2px; border-left: none; border-top: none; }
```

## 🌈 Theme Variations

### Light Theme (Default)
```css
:root {
  --bg-primary: linear-gradient(135deg, #F8FFF4 0%, #E8F5E8 100%);
  --surface-primary: rgba(255, 255, 255, 0.8);
  --text-primary: #1A1A1A;
  --text-secondary: #666666;
}
```

### Dark Theme
```css
[data-theme="dark"] {
  --bg-primary: linear-gradient(135deg, #0F1A0A 0%, #1A2F0F 100%);
  --surface-primary: rgba(45, 80, 22, 0.3);
  --text-primary: #FFFFFF;
  --text-secondary: #CCCCCC;
}
```

## 📱 Responsive Breakpoints

```css
/* Mobile First Approach */
.container {
  padding: var(--space-md);
  max-width: 100%;
}

/* Small phones */
@media (max-width: 375px) {
  .container { padding: var(--space-sm); }
  .glass-card { border-radius: var(--radius-md); }
}

/* Large phones */
@media (min-width: 414px) {
  .container { padding: var(--space-lg); }
  .status-grid { grid-template-columns: repeat(3, 1fr); }
}

/* Tablets */
@media (min-width: 768px) {
  .container { 
    max-width: 600px; 
    margin: 0 auto; 
  }
}
```

## 🎨 Icon System

### Icon Style Guidelines
- **Style**: Outline icons with 2px stroke
- **Size**: 24px default, 20px small, 32px large
- **Color**: Inherit from parent or use accent colors
- **Animation**: Subtle hover effects and state changes

### Primary Icons
```
🏠 Home - House outline
📷 Camera - Camera outline  
📊 Analytics - Chart bar
🌱 Plants - Leaf outline
👤 Profile - User circle
🔔 Notifications - Bell
⚙️ Settings - Cog
🎯 Scan - Target
💡 Tips - Light bulb
🌡️ Weather - Cloud sun
```

## 🚀 Implementation Notes

### Performance Optimizations
- Use `transform` and `opacity` for animations
- Implement `will-change` for animated elements
- Optimize backdrop-filter usage
- Use CSS containment for isolated components

### Accessibility
- Minimum 44px touch targets
- High contrast ratios (4.5:1 minimum)
- Focus indicators for keyboard navigation
- Screen reader friendly labels
- Reduced motion support

### Platform Considerations
- iOS: Use SF Pro Display font
- Android: Use Inter or system font
- Handle safe areas and notches
- Optimize for different screen densities

This design system creates a premium, nature-inspired agricultural app with modern glassmorphism aesthetics while maintaining excellent usability and accessibility standards.