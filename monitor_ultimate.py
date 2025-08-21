#!/usr/bin/env python3
"""
Monitor ultimate voice deployment progress - targeting ALL 78+ voices
"""

import requests
import time
import json

def check_voices():
    try:
        response = requests.get('https://binary-piper-tts-production.up.railway.app/voices', timeout=10)
        if response.status_code == 200:
            voices = response.json()
            return len(voices), voices
    except:
        pass
    return 0, []

def main():
    print("🚀 ULTIMATE Voice Collection Monitor")
    print("🎯 Target: ALL 78+ voices (based on your 73-voice local collection)")
    print("=" * 60)
    
    prev_count = 0
    stable_count = 0
    
    for i in range(20):  # Monitor for longer period
        print(f"\n📊 Check {i+1}/20...")
        
        voice_count, voices = check_voices()
        
        if voice_count > 0:
            if voice_count != prev_count:
                stable_count = 0
                print(f"🎵 Voices loaded: {voice_count} (+{voice_count - prev_count})")
            else:
                stable_count += 1
                print(f"🎵 Voices stable: {voice_count}")
            
            # Progress analysis
            if voice_count >= 70:
                print("🏆 ULTIMATE SUCCESS: 70+ voices achieved!")
            elif voice_count >= 60:
                print("🚀 EXCELLENT: 60+ voices!")
            elif voice_count >= 50:
                print("✅ GREAT: 50+ voices!")
            elif voice_count >= 45:
                print("📈 GOOD PROGRESS: 45+ voices!")
            elif voice_count > prev_count:
                print("📊 BUILDING: Good progress...")
            
            # Check if deployment is complete
            if stable_count >= 3 and voice_count >= 45:
                print(f"\n🎯 DEPLOYMENT COMPLETE: {voice_count} voices")
                
                # Show some example voices
                if voices:
                    print(f"\n📋 Sample voices loaded:")
                    for i, voice in enumerate(voices[:10]):
                        print(f"   • {voice}")
                    if len(voices) > 10:
                        print(f"   ... and {len(voices) - 10} more voices")
                break
            
            prev_count = voice_count
        else:
            print("⏳ Railway still building...")
        
        time.sleep(30)  # Check every 30 seconds
    
    print(f"\n🎯 Final Result: {voice_count} voices loaded")
    if voice_count >= 70:
        print("🏆 ULTIMATE SUCCESS - Nearly complete collection!")
    elif voice_count >= 60:
        print("🚀 EXCELLENT RESULT - Massive voice expansion!")

if __name__ == "__main__":
    main()
