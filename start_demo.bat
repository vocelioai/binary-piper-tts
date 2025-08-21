@echo off
echo 🎙️ Binary Piper TTS - Quick Start Demo
echo ====================================

echo 🚀 Starting TTS service with Web UI...
cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo ❌ Virtual environment not found!
    echo Please run setup first:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)

echo ⏳ Launching service...
start "TTS Service" /min venv\Scripts\python.exe -m uvicorn app:app --host 127.0.0.1 --port 8000

echo ⏳ Waiting for service to initialize...
timeout /t 8 /nobreak >nul

echo 🌐 Opening web interface...
start http://127.0.0.1:8000

echo.
echo ✅ Demo is ready!
echo ==================
echo 🌐 Web UI: http://127.0.0.1:8000
echo 📚 API Docs: http://127.0.0.1:8000/docs
echo 📊 Service Info: http://127.0.0.1:8000/api
echo.
echo ✨ Features:
echo   • 73 voices across 36 languages
echo   • Real-time speech synthesis
echo   • Voice search and filtering
echo   • Audio download (WAV format)
echo.
echo 🎯 Quick Demo Steps:
echo   1. Enter text or click language examples
echo   2. Search for a voice (try "english" or "spanish")
echo   3. Select a voice from the grid
echo   4. Click "Generate Speech"
echo   5. Listen or download the audio
echo.
echo Press any key to close this window...
echo The TTS service will continue running in the background.
pause >nul
