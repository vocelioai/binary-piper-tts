#!/usr/bin/env python3

import time
import requests
import json

def monitor_chunked_deployment():
    """Monitor the chunked deployment progress"""
    url = "https://binary-piper-tts-production.up.railway.app"
    
    print("🔍 MONITORING CHUNKED DEPLOYMENT")
    print("=" * 50)
    
    max_attempts = 20  # Monitor for ~10 minutes
    attempt = 0
    last_count = 0
    
    while attempt < max_attempts:
        try:
            # Health check
            health_response = requests.get(f"{url}/health", timeout=30)
            if health_response.status_code != 200:
                print(f"⏳ Attempt {attempt + 1}: Deployment not ready yet...")
                time.sleep(30)
                attempt += 1
                continue
            
            # Get voices count
            voices_response = requests.get(f"{url}/voices", timeout=30)
            if voices_response.status_code == 200:
                voices_data = voices_response.json()
                current_count = len(voices_data.get("voices", []))
                
                if current_count != last_count:
                    print(f"📈 Voice count update: {current_count} voices loaded")
                    
                    if current_count >= 50:
                        print(f"🎯 TARGET ACHIEVED! {current_count} voices loaded!")
                        return current_count
                    elif current_count >= 45:
                        print(f"🚀 EXCELLENT: {current_count} voices - Close to target!")
                    elif current_count >= 40:
                        print(f"✅ GOOD: {current_count} voices - Great progress!")
                    elif current_count >= 35:
                        print(f"📊 PROGRESS: {current_count} voices - Moving forward!")
                    
                    last_count = current_count
                else:
                    print(f"⏱️  Stable at {current_count} voices")
            
            time.sleep(30)
            attempt += 1
            
        except Exception as e:
            print(f"❌ Monitoring error: {e}")
            time.sleep(30)
            attempt += 1
    
    print(f"📊 Final monitoring result: {last_count} voices")
    return last_count

if __name__ == "__main__":
    final_count = monitor_chunked_deployment()
    if final_count >= 50:
        print("🎉 SUCCESS: 50+ voices achieved!")
    elif final_count >= 45:
        print("🌟 EXCELLENT: Close to 50+ voices target!")
    else:
        print(f"📈 Progress made: {final_count} voices loaded")
