#!/usr/bin/env python3
"""
🚀 Smart Voice Preloading Demo
Test the performance enhancement features of the Binary Piper TTS service
"""

import requests
import time
import json

BASE_URL = "http://127.0.0.1:8000"

def test_preloading_feature():
    """Test the smart voice preloading functionality"""
    
    print("🚀 Smart Voice Preloading Demo")
    print("=" * 50)
    
    # Step 1: Check initial cache stats
    print("\n📊 Step 1: Initial Cache Statistics")
    try:
        response = requests.get(f"{BASE_URL}/cache/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"🗄️  Initial Cache: {stats['audio_cache']['entries']}/{stats['audio_cache']['max_entries']} entries")
            print(f"📝 Memory Usage: {stats['audio_cache']['memory_usage_mb']}/{stats['audio_cache']['max_memory_mb']}MB")
            print(f"🎵 Total Usage: {stats['voice_manager']['total_usage_tracked']} requests")
            print(f"⭐ Popular Voices: {', '.join(stats['voice_manager']['popular_voices'][:3]) if stats['voice_manager']['popular_voices'] else 'None yet'}")
        else:
            print(f"❌ Failed to get initial stats: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error getting initial stats: {e}")
        return
    
    # Step 2: Preload popular voices
    print("\n🚀 Step 2: Preloading Popular Voices")
    voices_to_preload = ["en_US-danny-low", "en_US-lessac-medium", "es_ES-davefx-medium"]
    
    try:
        response = requests.post(
            f"{BASE_URL}/cache/preload",
            json=voices_to_preload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Preloading successful!")
            print(f"🎵 Voices preloaded: {', '.join(result['preloaded_voices'])}")
            print(f"📝 Status: {result['message']}")
        else:
            print(f"❌ Preloading failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error during preloading: {e}")
    
    # Step 3: Check updated cache stats
    print("\n📊 Step 3: Updated Cache Statistics")
    try:
        response = requests.get(f"{BASE_URL}/cache/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"🗄️  Updated Cache: {stats['audio_cache']['entries']}/{stats['audio_cache']['max_entries']} entries")
            print(f"📝 Memory Usage: {stats['audio_cache']['memory_usage_mb']}/{stats['audio_cache']['max_memory_mb']}MB")
            print(f"🎵 Total Usage: {stats['voice_manager']['total_usage_tracked']} requests")
            print(f"⭐ Popular Voices: {', '.join(stats['voice_manager']['popular_voices'][:5])}")
        else:
            print(f"❌ Failed to get updated stats: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting updated stats: {e}")
    
    # Step 4: Test synthesis performance
    print("\n⚡ Step 4: Testing Synthesis Performance")
    test_text = "Welcome to Vocelio.ai! How can I help you today?"
    
    # Test with preloaded voice
    print(f"\n🎵 Testing with preloaded voice: en_US-danny-low")
    try:
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/synthesize",
            json={
                "text": test_text,
                "voice": "en_US-danny-low",
                "speed": 1.0,
                "quality": "standard"
            },
            headers={"Content-Type": "application/json"}
        )
        end_time = time.time()
        
        if response.status_code == 200:
            processing_time = response.headers.get('X-Processing-Time', 'Unknown')
            cache_source = response.headers.get('X-Cache-Source', 'Unknown')
            
            print(f"✅ Synthesis successful!")
            print(f"⏱️  Request time: {(end_time - start_time):.3f}s")
            print(f"🔧 Processing time: {processing_time}")
            print(f"💾 Cache source: {cache_source}")
            print(f"📊 Audio size: {len(response.content):,} bytes")
        else:
            print(f"❌ Synthesis failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error during synthesis: {e}")
    
    # Step 5: Test cached response (repeat same request)
    print(f"\n🎯 Step 5: Testing Cache Hit (same request)")
    try:
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/synthesize",
            json={
                "text": test_text,
                "voice": "en_US-danny-low",
                "speed": 1.0,
                "quality": "standard"
            },
            headers={"Content-Type": "application/json"}
        )
        end_time = time.time()
        
        if response.status_code == 200:
            processing_time = response.headers.get('X-Processing-Time', 'Unknown')
            cache_source = response.headers.get('Cache-Source', response.headers.get('X-Cache-Source', 'Unknown'))
            
            print(f"✅ Cached synthesis successful!")
            print(f"⚡ Request time: {(end_time - start_time):.3f}s")
            print(f"🔧 Processing time: {processing_time}")
            print(f"💾 Cache source: {cache_source}")
            print(f"🎯 Expected: This should be MUCH faster (cache hit)!")
        else:
            print(f"❌ Cached synthesis failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error during cached synthesis: {e}")
    
    print("\n🎉 Smart Preloading Demo Complete!")
    print("=" * 50)
    print("💡 Key Benefits:")
    print("   • Popular voices are preloaded for faster response")
    print("   • Identical requests return in ~0.001s (cached)")
    print("   • Memory usage is efficiently managed")
    print("   • Voice usage patterns are automatically tracked")

if __name__ == "__main__":
    test_preloading_feature()
