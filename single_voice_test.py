#!/usr/bin/env python3
"""
Simple TTS Service Test - Single Voice Validation
"""
import requests
import json
import time
from pathlib import Path

def test_single_voice():
    """Test one voice to validate the service works"""
    print("🎯 Testing Single Voice - en_US-lessac-medium")
    
    try:
        # Test synthesis
        payload = {
            "text": "Hello! This is a test of the Binary Piper TTS service. Testing voice synthesis functionality.",
            "voice": "en_US-lessac-medium"
        }
        
        print("📤 Sending synthesis request...")
        response = requests.post(
            "http://localhost:8000/synthesize",
            json=payload,
            timeout=30,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            # Save the audio
            output_file = "single_voice_test.wav"
            with open(output_file, "wb") as f:
                f.write(response.content)
            
            file_size = Path(output_file).stat().st_size
            print(f"✅ SUCCESS! Audio generated: {output_file}")
            print(f"   📦 File size: {file_size:,} bytes")
            print(f"   🎵 Voice: en_US-lessac-medium")
            return True
        else:
            print(f"❌ FAILED: HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Binary Piper TTS - Single Voice Test")
    print("=" * 50)
    
    success = test_single_voice()
    
    if success:
        print("\n🎉 Single voice test PASSED!")
        print("The TTS service is working correctly.")
    else:
        print("\n💥 Single voice test FAILED!")
        print("There may be an issue with the service.")
    
    exit(0 if success else 1)
