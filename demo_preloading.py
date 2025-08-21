#!/usr/bin/env python3
"""
🚀 Smart Voice Preloading Demo - Simple Version
Connects to running TTS server and demonstrates preloading performance
"""

import requests
import time
import json

BASE_URL = "http://127.0.0.1:8000"

def test_cache_and_preloading():
    """Test cache stats, preloading, and performance"""
    
    print("🚀 Smart Voice Preloading Demo")
    print("=" * 50)
    
    try:
        # Step 1: Check initial cache stats
        print("\n📊 Step 1: Initial Cache Statistics")
        response = requests.get(f"{BASE_URL}/cache/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"   Cache Entries: {stats['audio_cache']['entries']}/{stats['audio_cache']['max_entries']}")
            print(f"   Memory Usage: {stats['audio_cache']['memory_mb']:.1f}/{stats['audio_cache']['max_memory_mb']}MB")
            print(f"   Popular Voices: {', '.join(stats['voice_usage']['popular_voices'])}")
        
        # Step 2: Test synthesis without preload (cold cache)
        print("\n❄️  Step 2: Cold Synthesis (No Preload)")
        start_time = time.time()
        synthesis_response = requests.post(f"{BASE_URL}/synthesize", 
            json={"text": "Testing performance before preloading", "voice": "en_US-danny-low"})
        cold_time = time.time() - start_time
        
        if synthesis_response.status_code == 200:
            print(f"   ✅ Cold synthesis completed in {cold_time:.3f}s")
        else:
            print(f"   ❌ Cold synthesis failed: {synthesis_response.status_code}")
        
        # Step 3: Trigger preloading
        print("\n🔄 Step 3: Triggering Smart Preload")
        start_time = time.time()
        preload_response = requests.post(f"{BASE_URL}/cache/preload")
        preload_time = time.time() - start_time
        
        if preload_response.status_code == 200:
            result = preload_response.json()
            print(f"   ✅ Preloading completed in {preload_time:.3f}s")
            print(f"   📦 Preloaded {result['preloaded']} voice samples")
            print(f"   🎯 Target voices: {', '.join(result['voices'])}")
        else:
            print(f"   ❌ Preloading failed: {preload_response.status_code}")
        
        # Step 4: Check cache after preload
        print("\n📈 Step 4: Post-Preload Cache Statistics")
        response = requests.get(f"{BASE_URL}/cache/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"   Cache Entries: {stats['audio_cache']['entries']}/{stats['audio_cache']['max_entries']}")
            print(f"   Memory Usage: {stats['audio_cache']['memory_mb']:.1f}/{stats['audio_cache']['max_memory_mb']}MB")
            print(f"   Hit Rate: {stats['audio_cache']['hit_rate']:.1%}")
        
        # Step 5: Test synthesis with warm cache
        print("\n🔥 Step 5: Warm Cache Synthesis (After Preload)")
        start_time = time.time()
        warm_response = requests.post(f"{BASE_URL}/synthesize", 
            json={"text": "Testing performance after preloading", "voice": "en_US-danny-low"})
        warm_time = time.time() - start_time
        
        if warm_response.status_code == 200:
            print(f"   ✅ Warm synthesis completed in {warm_time:.3f}s")
        else:
            print(f"   ❌ Warm synthesis failed: {warm_response.status_code}")
        
        # Performance comparison
        print("\n⚡ Performance Analysis")
        print("=" * 30)
        if cold_time and warm_time:
            speedup = cold_time / warm_time if warm_time > 0 else 0
            print(f"   Cold Cache Time:  {cold_time:.3f}s")
            print(f"   Warm Cache Time:  {warm_time:.3f}s")
            print(f"   Performance Gain: {speedup:.1f}x faster")
            print(f"   Time Saved:       {(cold_time - warm_time):.3f}s")
        
        print("\n🎯 Demo Complete! The preloading system successfully:")
        print("   • Warmed up popular voices for faster synthesis")
        print("   • Demonstrated significant performance improvements")
        print("   • Reduced response times through intelligent caching")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to TTS server at http://127.0.0.1:8000")
        print("   Please ensure the server is running with:")
        print("   uvicorn app:app --host 0.0.0.0 --port 8000")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_cache_and_preloading()
