#!/usr/bin/env python3
"""
Railway setup script for Binary Piper TTS
Downloads Piper binary and sets up environment
"""
import os
import subprocess
import urllib.request
import tarfile
import shutil
from pathlib import Path

def setup_piper():
    """Download and install Piper binary"""
    print("🔧 Setting up Piper binary...")
    
    # Download Piper
    piper_url = "https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz"
    
    print(f"📥 Downloading from {piper_url}")
    urllib.request.urlretrieve(piper_url, "piper.tar.gz")
    
    # Extract
    print("📦 Extracting Piper binary...")
    with tarfile.open("piper.tar.gz", "r:gz") as tar:
        tar.extractall()
    
    # Move to system location
    piper_bin = Path("piper/piper")
    if piper_bin.exists():
        dest = Path("/usr/local/bin/piper")
        shutil.move(str(piper_bin), str(dest))
        dest.chmod(0o755)
        print(f"✅ Piper installed to {dest}")
    
    # Cleanup
    os.remove("piper.tar.gz")
    shutil.rmtree("piper", ignore_errors=True)

def install_system_deps():
    """Install system dependencies"""
    print("📦 Installing system dependencies...")
    subprocess.run([
        "apt-get", "update", "-y"
    ], check=True)
    
    subprocess.run([
        "apt-get", "install", "-y",
        "wget", "curl", "espeak-ng", "espeak-ng-data"
    ], check=True)

def main():
    print("🚀 Binary Piper TTS - Railway Setup")
    
    try:
        install_system_deps()
        setup_piper()
        
        # Create models directory
        Path("models").mkdir(exist_ok=True)
        
        print("✅ Setup complete! Ready to download voice models.")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        exit(1)

if __name__ == "__main__":
    main()
