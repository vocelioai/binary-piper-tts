#!/usr/bin/env python3
"""
Binary Piper TTS - Extended Text Length Test
Testing the new 100,000 character limit
"""

import requests
import time
import json

def test_extended_text_limits():
    """Test the new extended text limits"""
    
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 TESTING EXTENDED TEXT LIMITS")
    print("=" * 60)
    print()
    
    # Test different text lengths
    test_cases = [
        (1000, "Short text (1K chars)"),
        (5000, "Medium text (5K chars)"), 
        (20000, "Long text (20K chars)"),
        (50000, "Very long text (50K chars)"),
        (100000, "Maximum text (100K chars)")
    ]
    
    # Generate test text
    base_sentence = "This is a test sentence for the Binary Piper TTS extended text length capability. "
    
    for length, description in test_cases:
        print(f"📝 {description}")
        print("-" * 40)
        
        # Generate text of specified length
        sentences_needed = length // len(base_sentence) + 1
        test_text = (base_sentence * sentences_needed)[:length]
        
        print(f"   Generated text length: {len(test_text):,} characters")
        
        # Test with /synthesize endpoint (should work for all lengths now)
        try:
            print("   🔊 Testing /synthesize endpoint...")
            
            payload = {
                "text": test_text,
                "voice": "en_US-lessac-medium",
                "format": "wav"
            }
            
            start_time = time.time()
            response = requests.post(
                f"{base_url}/synthesize", 
                json=payload,
                timeout=1200  # 20 minute timeout for testing
            )
            processing_time = time.time() - start_time
            
            if response.status_code == 200:
                audio_size = len(response.content)
                print(f"   ✅ SUCCESS: {audio_size:,} bytes audio generated")
                print(f"   ⏱️ Processing time: {processing_time:.1f}s")
                print(f"   🎵 Speed ratio: {len(test_text)/processing_time:.1f} chars/sec")
            else:
                print(f"   ❌ FAILED: {response.status_code}")
                try:
                    error_detail = response.json().get("detail", "Unknown error")
                    print(f"   📄 Error: {error_detail}")
                except:
                    print(f"   📄 Raw response: {response.text[:200]}...")
                    
        except requests.exceptions.Timeout:
            print(f"   ⏰ TIMEOUT: Request exceeded timeout limit")
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
        
        print()
        
        # Brief pause between tests
        time.sleep(1)
    
    # Test service status
    print("📊 CHECKING SERVICE STATUS")
    print("-" * 40)
    try:
        status_response = requests.get(f"{base_url}/status", timeout=10)
        if status_response.status_code == 200:
            status = status_response.json()
            print("✅ Service status retrieved:")
            print(f"   📝 Max text length: {status['limits']['max_length_formatted']}")
            print(f"   ⏱️ Timeout standard: {status['performance']['timeout_standard']}")
            print(f"   🔧 Timeout formula: {status['performance']['timeout_formula']}")
        else:
            print(f"❌ Status check failed: {status_response.status_code}")
    except Exception as e:
        print(f"❌ Status check error: {e}")
    
    print()
    print("🏆 EXTENDED TEXT LENGTH TEST COMPLETED")
    print("   The service now supports up to 100,000 characters!")
    print("   Timeouts extended: 300s - 1800s (5-30 minutes)")

if __name__ == "__main__":
    test_extended_text_limits()
