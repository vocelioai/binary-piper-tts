#!/usr/bin/env python3
"""Test Piper binary directly to verify TTS functionality"""

import subprocess
import os
import sys

def test_piper_binary():
    """Test the Piper binary directly"""
    
    # Paths
    piper_binary = r"C:\Users\SNC\binary-piper-tts\piper-bin\piper\piper.exe"
    models_dir = r"C:\Users\SNC\binary-piper-tts\models"
    
    # Check if binary exists
    if not os.path.exists(piper_binary):
        print(f"❌ Piper binary not found at: {piper_binary}")
        return False
    
    print(f"✅ Piper binary found: {piper_binary}")
    
    # Check models directory
    if not os.path.exists(models_dir):
        print(f"❌ Models directory not found at: {models_dir}")
        return False
        
    print(f"✅ Models directory found: {models_dir}")
    
    # Find first available voice
    voice_found = None
    for file in os.listdir(models_dir):
        if file.endswith('.onnx'):
            voice_found = file.replace('.onnx', '')
            break
    
    if not voice_found:
        print("❌ No voice models found in models directory")
        return False
        
    print(f"✅ Found voice model: {voice_found}")
    
    # Test TTS synthesis
    test_text = "Hello world, this is a test of the Binary Piper text to speech system."
    model_path = os.path.join(models_dir, f"{voice_found}.onnx")
    output_file = "direct_test_output.wav"
    
    try:
        print(f"🎙️ Testing synthesis with text: '{test_text}'")
        
        # Build command
        cmd = [
            piper_binary,
            "--model", model_path,
            "--output_file", output_file
        ]
        
        # Run Piper
        result = subprocess.run(
            cmd,
            input=test_text,
            text=True,
            capture_output=True,
            timeout=30
        )
        
        if result.returncode == 0:
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file)
                print(f"✅ Synthesis successful!")
                print(f"   📄 Output file: {output_file}")
                print(f"   📊 File size: {file_size} bytes")
                return True
            else:
                print("❌ Synthesis completed but no output file created")
                return False
        else:
            print(f"❌ Piper command failed with return code: {result.returncode}")
            print(f"   stdout: {result.stdout}")
            print(f"   stderr: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Piper command timed out")
        return False
    except Exception as e:
        print(f"❌ Error running Piper: {e}")
        return False

def list_available_voices():
    """List all available voice models"""
    models_dir = r"C:\Users\SNC\binary-piper-tts\models"
    
    if not os.path.exists(models_dir):
        print("❌ Models directory not found")
        return []
    
    voices = []
    for file in os.listdir(models_dir):
        if file.endswith('.onnx'):
            voices.append(file.replace('.onnx', ''))
    
    voices.sort()
    print(f"\n📋 Found {len(voices)} voice models:")
    for i, voice in enumerate(voices, 1):
        print(f"   {i:2d}. {voice}")
    
    return voices

if __name__ == "__main__":
    print("🔧 Testing Binary Piper TTS directly...")
    
    # List available voices
    voices = list_available_voices()
    
    if voices:
        print(f"\n🎯 Testing with first available voice...")
        success = test_piper_binary()
        
        if success:
            print("\n✅ Direct Piper test completed successfully!")
            print("   The TTS system is working correctly.")
        else:
            print("\n❌ Direct Piper test failed!")
    else:
        print("\n❌ No voice models available for testing!")
        sys.exit(1)
