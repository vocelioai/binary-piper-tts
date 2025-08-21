#!/usr/bin/env python3

import requests
import json

def check_railway_diagnostics():
    """Check Railway deployment for voice loading diagnostics"""
    
    base_url = "https://binary-piper-tts-production.up.railway.app"
    
    print("🔍 RAILWAY VOICE DIAGNOSTICS")
    print("=" * 50)
    
    try:
        # Check if we can add a diagnostics endpoint
        diag_response = requests.get(f"{base_url}/diagnostics", timeout=30)
        if diag_response.status_code == 200:
            print("✅ Diagnostics endpoint available")
            print(diag_response.text)
        else:
            print("❌ No diagnostics endpoint, checking standard endpoints...")
            
            # Check health
            health_response = requests.get(f"{base_url}/health", timeout=30)
            if health_response.status_code == 200:
                health_data = health_response.json()
                print(f"✅ Health: {health_data}")
            
            # Check voices
            voices_response = requests.get(f"{base_url}/voices", timeout=30)
            if voices_response.status_code == 200:
                voices = voices_response.json()
                print(f"🎵 Loaded voices: {len(voices)}")
                
                # Test a sample voice
                if voices:
                    test_voice = voices[0]
                    test_response = requests.post(
                        f"{base_url}/synthesize",
                        json={"text": "Test", "voice": test_voice},
                        timeout=30
                    )
                    print(f"🔧 Test synthesis with {test_voice}: {test_response.status_code}")
            
    except Exception as e:
        print(f"❌ Railway diagnostics failed: {e}")

if __name__ == "__main__":
    check_railway_diagnostics()
