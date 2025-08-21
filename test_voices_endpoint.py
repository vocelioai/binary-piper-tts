#!/usr/bin/env python3
"""Quick test to verify the voices endpoint format"""

import requests
import json

def test_voices_endpoint():
    """Test the /voices endpoint format"""
    try:
        print("🔍 Testing /voices endpoint...")
        response = requests.get("http://127.0.0.1:8000/voices", timeout=10)
        
        if response.status_code == 200:
            voices = response.json()
            
            print(f"✅ Status: {response.status_code}")
            print(f"✅ Response type: {type(voices)}")
            print(f"✅ Is iterable: {'Yes' if hasattr(voices, '__iter__') else 'No'}")
            
            if isinstance(voices, list):
                print(f"✅ Voice count: {len(voices)}")
                print(f"✅ First 5 voices: {voices[:5]}")
                print("✅ Endpoint format is correct for web UI!")
                return True
            else:
                print(f"❌ Expected list, got: {type(voices)}")
                print(f"   Response: {voices}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    success = test_voices_endpoint()
    if success:
        print("\n🎉 Voices endpoint test PASSED!")
    else:
        print("\n❌ Voices endpoint test FAILED!")
