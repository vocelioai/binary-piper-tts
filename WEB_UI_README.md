# 🎙️ Binary Piper TTS - Web Interface

A modern, user-friendly web interface for testing and demonstrating the Binary Piper TTS service.

## ✨ Features

### 🎯 **Easy Voice Testing**
- **73 High-Quality Voices** across 36 languages
- **Live Voice Search** - Find voices by name or language
- **Language-Specific Examples** - Quick test phrases in multiple languages
- **Real-time Audio Preview** - Instant playback of generated speech

### 🌍 **Multi-Language Support**
- Arabic, Chinese, German, Spanish, French, Russian, Italian, Portuguese
- Dutch, Polish, Turkish, Ukrainian, Vietnamese, and 24+ more languages
- Native test phrases for authentic pronunciation testing

### 💫 **Modern User Experience**
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Real-time Status** - Live service health monitoring
- **Progress Indicators** - Visual feedback during synthesis
- **Audio Download** - Save generated speech as WAV files

### 🔧 **Developer Friendly**
- **Service Health Dashboard** - Monitor voices loaded and system status
- **Performance Metrics** - View synthesis time and audio file sizes
- **Error Handling** - Clear error messages and troubleshooting tips
- **API Integration** - Direct connection to TTS service endpoints

## 🚀 Quick Start

1. **Start the TTS Service:**
   ```bash
   cd C:\Users\SNC\binary-piper-tts
   venv\Scripts\activate
   uvicorn app:app --host 127.0.0.1 --port 8000
   ```

2. **Open Web Interface:**
   - Navigate to: http://127.0.0.1:8000
   - The web UI will load automatically

3. **Test Voice Synthesis:**
   - Enter text to synthesize
   - Select from 73 available voices
   - Click "Generate Speech" to create audio
   - Play, download, or test different voices

## 🎭 Voice Selection Guide

### **Search and Filter**
- Type in the search box to filter voices by:
  - Language code (e.g., "en", "es", "fr")
  - Voice name (e.g., "amy", "thorsten", "natia")
  - Quality level ("high", "medium", "low")

### **Voice Naming Convention**
```
[language]_[region]-[name]-[quality]
```

Examples:
- `en_US-lessac-high` - English (US), Lessac voice, high quality
- `es_ES-davefx-medium` - Spanish (Spain), Davefx voice, medium quality
- `fr_FR-siwis-low` - French (France), Siwis voice, low quality

### **Quality Levels**
- **HIGH** - Best quality, larger files, slower synthesis
- **MEDIUM** - Balanced quality and speed
- **LOW** - Faster synthesis, smaller files

## 🌍 Supported Languages (36 total)

| Language | Code | Voices | Example Text Available |
|----------|------|---------|----------------------|
| Arabic | `ar` | 2 | ✅ |
| Catalan | `ca` | 2 | ✅ |
| Chinese | `zh` | 1 | ✅ |
| Czech | `cs` | 2 | ✅ |
| Danish | `da` | 1 | ✅ |
| Dutch | `nl` | 3 | ✅ |
| English | `en` | 16 | ✅ |
| Finnish | `fi` | 1 | ✅ |
| French | `fr` | 4 | ✅ |
| German | `de` | 6 | ✅ |
| Greek | `el` | 1 | ✅ |
| Hungarian | `hu` | 1 | ✅ |
| Icelandic | `is` | 2 | ✅ |
| Italian | `it` | 2 | ✅ |
| Polish | `pl` | 3 | ✅ |
| Portuguese | `pt` | 1 | ✅ |
| Russian | `ru` | 3 | ✅ |
| Spanish | `es` | 5 | ✅ |
| Turkish | `tr` | 2 | ✅ |
| ...and 17 more | | | |

## 🎨 Interface Components

### **Status Bar**
- **Green Dot** 🟢 - Service online and healthy
- **Red Dot** 🔴 - Service offline or unhealthy
- **Voice Count** - Shows total loaded voices (should show 73)
- **Language Count** - Shows supported languages (should show 36)

### **Text Input**
- **Multi-line Text Area** - Enter any text up to 1000 characters
- **Quick Examples** - Pre-defined text in multiple languages
- **Character Counter** - Real-time text length tracking

### **Voice Selection**
- **Visual Grid** - Easy-to-browse voice options
- **Language Badges** - Color-coded language indicators
- **Quality Indicators** - HIGH/MED/LOW quality levels
- **Search Function** - Real-time voice filtering

### **Results Section**
- **Audio Player** - Built-in playback controls
- **Download Button** - Save audio as WAV file
- **Metadata Display** - File size, synthesis time, voice info
- **Error Messages** - Clear troubleshooting information

## 🔧 Troubleshooting

### **Service Connection Issues**
- **Red Status Dot**: Service is not running
- **Solution**: Start the TTS service with `uvicorn app:app --host 127.0.0.1 --port 8000`

### **No Voices Available**
- **Cause**: Voice models not loaded
- **Solution**: Check that models directory contains .onnx files

### **Synthesis Fails**
- **Text Too Long**: Reduce text to under 1000 characters
- **Invalid Voice**: Select a voice from the grid
- **Service Timeout**: Try shorter text or restart service

### **Audio Playback Issues**
- **No Audio**: Check browser audio permissions
- **Format Error**: Download WAV file and play with external player
- **Quality Issues**: Try different voice or quality level

## 🔗 API Endpoints (for developers)

The web UI interacts with these service endpoints:

- `GET /health` - Service health check
- `GET /voices` - List all available voices
- `POST /synthesize` - Generate speech from text
- `GET /api` - Service information and statistics
- `GET /` - Serve web UI (this interface)

## 💡 Tips for Best Results

1. **Choose Appropriate Voice**: Match voice language to text language
2. **Punctuation Matters**: Use periods, commas for natural speech rhythm
3. **Quality vs Speed**: High-quality voices take longer but sound better
4. **Text Length**: Shorter texts (under 200 chars) synthesize faster
5. **Language Examples**: Use provided examples for best pronunciation

## 🎉 Features in Action

### **Real-time Voice Testing**
1. Type or paste text
2. Search for desired voice (e.g., "english female")
3. Click voice to select
4. Hit "Generate Speech" 
5. Listen immediately or download

### **Multi-language Demonstration**
1. Click language example buttons (English, Español, Français, etc.)
2. Select matching language voice
3. Generate and compare different voices in same language
4. Experience authentic pronunciation across languages

### **Performance Monitoring**
- Synthesis time tracking
- Audio file size reporting
- Voice loading status
- Service health monitoring

---

**🎙️ Ready to explore 73 high-quality voices across 36 languages!**

Open http://127.0.0.1:8000 and start creating amazing speech synthesis!
