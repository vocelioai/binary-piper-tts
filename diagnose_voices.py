#!/usr/bin/env python3

import os
import glob
import requests
import json

def diagnose_voice_loading():
    """Diagnose voice loading issues - check files vs loaded voices"""
    
    print("🔍 VOICE LOADING DIAGNOSTICS")
    print("=" * 50)
    
    # Check local files
    model_files = glob.glob("models/*.onnx")
    json_files = glob.glob("models/*.onnx.json")
    
    print(f"📁 Local .onnx files found: {len(model_files)}")
    print(f"📁 Local .json files found: {len(json_files)}")
    
    if model_files:
        print("\n📋 Local model files:")
        for i, file in enumerate(sorted(model_files), 1):
            voice_id = os.path.basename(file).replace('.onnx', '')
            json_file = file + '.json'
            has_json = os.path.exists(json_file)
            size_mb = os.path.getsize(file) / (1024 * 1024)
            print(f"  {i:2d}. {voice_id} ({size_mb:.1f}MB) {'✅' if has_json else '❌ NO JSON'}")
    
    # Check what's loaded in the API
    try:
        response = requests.get("https://binary-piper-tts-production.up.railway.app/voices", timeout=30)
        if response.status_code == 200:
            loaded_voices = response.json()
            print(f"\n🎵 Voices loaded by API: {len(loaded_voices)}")
            
            # Find differences
            local_voice_ids = set()
            for file in model_files:
                voice_id = os.path.basename(file).replace('.onnx', '')
                local_voice_ids.add(voice_id)
            
            loaded_voice_ids = set(loaded_voices)
            
            missing_from_api = local_voice_ids - loaded_voice_ids
            extra_in_api = loaded_voice_ids - local_voice_ids
            
            if missing_from_api:
                print(f"\n❌ Downloaded but NOT loaded ({len(missing_from_api)}):")
                for voice in sorted(missing_from_api):
                    print(f"  - {voice}")
            
            if extra_in_api:
                print(f"\n❓ Loaded but no local file ({len(extra_in_api)}):")
                for voice in sorted(extra_in_api):
                    print(f"  - {voice}")
            
            if not missing_from_api and not extra_in_api:
                print("\n✅ All local files are loaded in API!")
        else:
            print(f"❌ API request failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ API check failed: {e}")
    
    # Check models directory structure
    print(f"\n📂 Models directory structure:")
    if os.path.exists("models"):
        for root, dirs, files in os.walk("models"):
            level = root.replace("models", "").count(os.sep)
            indent = " " * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = " " * 2 * (level + 1)
            for file in files[:10]:  # Show first 10 files
                print(f"{subindent}{file}")
            if len(files) > 10:
                print(f"{subindent}... and {len(files) - 10} more files")
    else:
        print("  ❌ models directory not found!")

if __name__ == "__main__":
    diagnose_voice_loading()
