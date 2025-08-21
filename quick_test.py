#!/usr/bin/env python3
"""Quick test to verify TTS service is working"""

import requests
import time
import json

def test_service():
    base_url = "http://127.0.0.1:8000"
    
    print("Testing Binary Piper TTS Service...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✓ Health check passed")
        else:
            print(f"✗ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False
    
    # Get voices list
    try:
        response = requests.get(f"{base_url}/voices", timeout=5)
        if response.status_code == 200:
            voices = response.json()
            print(f"✓ Found {len(voices)} voices")
            if len(voices) == 0:
                print("✗ No voices available")
                return False
        else:
            print(f"✗ Failed to get voices: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Failed to get voices: {e}")
        return False
    
    # Test synthesis with first available voice
    test_voice = voices[0]
    print(f"Testing synthesis with voice: {test_voice}")
    
    try:
        synthesis_data = {
            "text": "Hello world, this is a test of the text to speech system.",
            "voice": test_voice
        }
        
        response = requests.post(f"{base_url}/synthesize", 
                               json=synthesis_data, 
                               timeout=10)
        
        if response.status_code == 200:
            # Save audio file
            with open("test_output.wav", "wb") as f:
                f.write(response.content)
            print(f"✓ Synthesis successful - saved test_output.wav")
            print(f"  Audio file size: {len(response.content)} bytes")
            return True
        else:
            print(f"✗ Synthesis failed: {response.status_code}")
            if response.content:
                print(f"  Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Synthesis failed: {e}")
        return False

if __name__ == "__main__":
    # Give service a moment to be ready
    print("Waiting 2 seconds for service to be ready...")
    time.sleep(2)
    
    success = test_service()
    if success:
        print("\n✓ Service test completed successfully!")
    else:
        print("\n✗ Service test failed!")
