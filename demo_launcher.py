#!/usr/bin/env python3
"""
Binary Piper TTS - Demo Launcher
Starts the TTS service and opens the web UI for easy demonstration
"""

import subprocess
import time
import webbrowser
import sys
import os
from pathlib import Path

def check_service_health():
    """Check if the TTS service is responding"""
    try:
        import requests
        response = requests.get("http://127.0.0.1:8000/health", timeout=5)
        return response.status_code == 200
    except Exception:
        return False

def start_demo():
    """Start the TTS service and open web browser"""
    print("🎙️ Binary Piper TTS - Demo Launcher")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("app.py"):
        print("❌ Error: Please run this script from the binary-piper-tts directory")
        print("   Current directory:", os.getcwd())
        return False
    
    # Check if virtual environment exists
    venv_python = Path("venv/Scripts/python.exe")  # Windows
    if not venv_python.exists():
        venv_python = Path("venv/bin/python")  # Linux/Mac
        
    if not venv_python.exists():
        print("❌ Error: Virtual environment not found")
        print("   Please run: python -m venv venv")
        print("   Then: venv\\Scripts\\activate (Windows) or source venv/bin/activate (Linux/Mac)")
        print("   Then: pip install -r requirements.txt")
        return False
    
    print("🚀 Starting TTS service...")
    
    # Start the service in background
    cmd = [str(venv_python), "-m", "uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8000"]
    
    try:
        # Start service process
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait for service to start
        print("⏳ Waiting for service to initialize...")
        for i in range(30):  # Wait up to 30 seconds
            time.sleep(1)
            if check_service_health():
                print("✅ Service is ready!")
                break
            print(f"   Loading voices... ({i+1}/30)")
        else:
            print("❌ Service failed to start within 30 seconds")
            process.terminate()
            return False
        
        # Open web browser
        web_url = "http://127.0.0.1:8000"
        print(f"🌐 Opening web interface: {web_url}")
        webbrowser.open(web_url)
        
        print("\n" + "=" * 50)
        print("🎉 DEMO READY!")
        print("=" * 50)
        print(f"Web UI: {web_url}")
        print("API Docs: http://127.0.0.1:8000/docs")
        print("Service Info: http://127.0.0.1:8000/api")
        print("\n✨ Features available:")
        print("   • 73 high-quality voices")
        print("   • 36 different languages")
        print("   • Real-time synthesis")
        print("   • Audio download")
        print("   • Voice search & filtering")
        print("\n🔍 Try these demo steps:")
        print("   1. Type some text or click a language example")
        print("   2. Search for a voice (try 'english', 'spanish', 'french')")
        print("   3. Click on a voice to select it")
        print("   4. Hit 'Generate Speech' to create audio")
        print("   5. Play the audio or download the WAV file")
        print("\n⚠️  Press Ctrl+C to stop the service")
        
        try:
            # Keep the service running
            process.wait()
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping service...")
            process.terminate()
            process.wait()
            print("✅ Service stopped successfully")
            
    except KeyboardInterrupt:
        print("\n\n🛑 Demo interrupted")
        return False
    except Exception as e:
        print(f"❌ Error starting demo: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = start_demo()
    sys.exit(0 if success else 1)
