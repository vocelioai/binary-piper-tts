#!/usr/bin/env python3

import requests
import json
from collections import defaultdict

def analyze_all_voices():
    """Get comprehensive analysis of all deployed voices"""
    url = "https://binary-piper-tts-production.up.railway.app/voices"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        voices = response.json()
        
        print("🔍 COMPREHENSIVE VOICE ANALYSIS")
        print("=" * 60)
        print(f"📊 Total voices deployed: {len(voices)}")
        print()
        
        # Group by language/region
        language_groups = defaultdict(list)
        quality_groups = defaultdict(list)
        
        for voice in voices:
            # Extract language code (first part before hyphen)
            lang_code = voice.split('-')[0]
            language_groups[lang_code].append(voice)
            
            # Extract quality (last part after last hyphen)
            quality = voice.split('-')[-1]
            quality_groups[quality].append(voice)
        
        print("🌍 VOICES BY LANGUAGE:")
        print("-" * 40)
        for lang, voices_list in sorted(language_groups.items()):
            print(f"{lang.upper()}: {len(voices_list)} voices")
            for voice in sorted(voices_list):
                print(f"  - {voice}")
        
        print(f"\n🎯 QUALITY DISTRIBUTION:")
        print("-" * 40)
        for quality, voices_list in sorted(quality_groups.items()):
            print(f"{quality.upper()}: {len(voices_list)} voices")
        
        print(f"\n📋 COMPLETE VOICE LIST:")
        print("-" * 40)
        for i, voice in enumerate(sorted(voices), 1):
            print(f"{i:2d}. {voice}")
        
        print(f"\n🎉 SUMMARY:")
        print("-" * 40)
        print(f"Total Voices: {len(voices)}")
        print(f"Languages: {len(language_groups)}")
        print(f"Quality Levels: {len(quality_groups)}")
        
        return voices
        
    except Exception as e:
        print(f"❌ Error analyzing voices: {e}")
        return []

if __name__ == "__main__":
    voices = analyze_all_voices()
