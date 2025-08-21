#!/usr/bin/env python3
"""
Test script for Binary Piper TTS Service
Tests various voices and functionalities
"""
import requests
import json
from pathlib import Path

BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health check passed: {health_data['status']}")
            print(f"   Voices loaded: {health_data['voices_loaded']}")
            print(f"   Binary path: {health_data['piper_binary']}")
            return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_voices_list():
    """Test the voices list endpoint"""
    print("\n🎙️ Testing voices list...")
    try:
        response = requests.get(f"{BASE_URL}/voices")
        if response.status_code == 200:
            voices = response.json()
            print(f"✅ Found {len(voices)} voices available")
            
            # Show some sample voices
            print("   Sample voices:")
            for i, voice in enumerate(voices[:5]):
                print(f"     {i+1}. {voice}")
            return voices
    except Exception as e:
        print(f"❌ Voices list failed: {e}")
        return []

def test_synthesis(voice="en_US-lessac-medium", text="Hello! This is a test of the Binary Piper TTS service."):
    """Test text-to-speech synthesis"""
    print(f"\n🔊 Testing synthesis with voice: {voice}")
    try:
        payload = {
            "text": text,
            "voice": voice
        }
        
        response = requests.post(
            f"{BASE_URL}/synthesize",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            # Save the audio file
            output_file = f"test_synthesis_{voice}.wav"
            with open(output_file, "wb") as f:
                f.write(response.content)
            
            file_size = Path(output_file).stat().st_size
            print(f"✅ Synthesis successful! Audio saved as {output_file}")
            print(f"   File size: {file_size:,} bytes")
            return True
        else:
            print(f"❌ Synthesis failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Synthesis error: {e}")
        return False

def test_multiple_voices():
    """Test synthesis with different voices"""
    print("\n🌍 Testing multiple voices...")
    test_voices = [
        ("en_US-lessac-medium", "Hello from English!"),
        ("de_DE-thorsten-medium", "Hallo aus Deutschland!"),
        ("fr_FR-siwis-medium", "Bonjour de France!"),
        ("es_ES-davefx-medium", "¡Hola desde España!"),
        ("it_IT-paola-medium", "Ciao dall'Italia!")
    ]
    
    success_count = 0
    for voice, text in test_voices:
        if test_synthesis(voice, text):
            success_count += 1
    
    print(f"\n📊 Multi-voice test results: {success_count}/{len(test_voices)} successful")

def main():
    """Run all tests"""
    print("🚀 Binary Piper TTS Service - Comprehensive Test Suite")
    print("=" * 60)
    
    # Test 1: Health check
    if not test_health():
        print("❌ Service not healthy, stopping tests")
        return
    
    # Test 2: Voices list
    voices = test_voices_list()
    if not voices:
        print("❌ No voices available, stopping tests")
        return
    
    # Test 3: Basic synthesis
    if not test_synthesis():
        print("❌ Basic synthesis failed")
        return
    
    # Test 4: Multiple voices
    test_multiple_voices()
    
    print("\n🎉 All tests completed!")
    print("\n📁 Generated audio files:")
    wav_files = list(Path(".").glob("test_synthesis_*.wav"))
    for wav_file in wav_files:
        size = wav_file.stat().st_size
        print(f"   • {wav_file.name} ({size:,} bytes)")

if __name__ == "__main__":
    main()
