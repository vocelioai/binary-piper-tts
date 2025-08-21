#!/usr/bin/env python3
"""
Minimal voice model downloader for Railway deployment
Downloads only essential voices for faster deployment
"""
import os
import urllib.request
import urllib.error
from pathlib import Path
import json

MODELS_DIR = Path("models")
MODELS_DIR.mkdir(exist_ok=True)

BASE_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/main"

# Essential voices for quick deployment
ESSENTIAL_VOICES = {
    "en_US-lessac-medium": {
        "urls": [
            f"{BASE_URL}/en/en_US/lessac/medium/en_US-lessac-medium.onnx",
            f"{BASE_URL}/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json"
        ]
    },
    "en_GB-cori-medium": {
        "urls": [
            f"{BASE_URL}/en/en_GB/cori/medium/en_GB-cori-medium.onnx",
            f"{BASE_URL}/en/en_GB/cori/medium/en_GB-cori-medium.onnx.json"
        ]
    },
    "es_ES-davefx-medium": {
        "urls": [
            f"{BASE_URL}/es/es_ES/davefx/medium/es_ES-davefx-medium.onnx",
            f"{BASE_URL}/es/es_ES/davefx/medium/es_ES-davefx-medium.onnx.json"
        ]
    },
    "fr_FR-siwis-medium": {
        "urls": [
            f"{BASE_URL}/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx",
            f"{BASE_URL}/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx.json"
        ]
    },
    "de_DE-thorsten-medium": {
        "urls": [
            f"{BASE_URL}/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx",
            f"{BASE_URL}/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx.json"
        ]
    }
}

def download_file(url, filepath):
    """Download a file with error handling"""
    try:
        print(f"Downloading {filepath.name}...")
        urllib.request.urlretrieve(url, filepath)
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def main():
    """Download essential voice models"""
    print("🚀 Downloading essential voice models for Railway...")
    
    downloaded = 0
    total = len(ESSENTIAL_VOICES)
    
    for voice_id, voice_data in ESSENTIAL_VOICES.items():
        print(f"\n📦 Downloading {voice_id}...")
        
        success = True
        for url in voice_data["urls"]:
            filename = url.split("/")[-1]
            filepath = MODELS_DIR / filename
            
            if not download_file(url, filepath):
                success = False
                break
        
        if success:
            downloaded += 1
            print(f"✅ {voice_id} downloaded successfully")
        else:
            print(f"❌ Failed to download {voice_id}")
    
    print(f"\n🎉 Download complete! {downloaded}/{total} voices ready")
    
    if downloaded == 0:
        print("⚠️ No voices downloaded - using fallback mode")
        # Create a dummy model for testing
        dummy_config = {
            "audio": {"sample_rate": 22050},
            "num_speakers": 1,
            "language": {"code": "en-us"}
        }
        with open(MODELS_DIR / "dummy.onnx.json", "w") as f:
            json.dump(dummy_config, f)
        
        # Create dummy model file
        with open(MODELS_DIR / "dummy.onnx", "wb") as f:
            f.write(b"dummy")

if __name__ == "__main__":
    main()
