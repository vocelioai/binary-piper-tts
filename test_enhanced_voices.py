#!/usr/bin/env python3
"""
Test the enhanced voice downloader locally
"""

import subprocess
import sys
import time

def test_enhanced_downloader():
    """Test the new enhanced voice downloader"""
    print("🧪 Testing Enhanced Voice Downloader")
    print("=" * 50)
    
    start_time = time.time()
    
    try:
        # Run the enhanced downloader
        result = subprocess.run([
            sys.executable, "download_models_enhanced.py"
        ], capture_output=True, text=True, timeout=600)
        
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            print("✅ Enhanced downloader completed successfully!")
            print(f"⏱️ Time taken: {elapsed:.1f} seconds")
            print("\n📊 Output:")
            print(result.stdout)
            
            # Check how many voices were downloaded
            import json
            try:
                with open("models/download_summary.json") as f:
                    summary = json.load(f)
                    
                print(f"\n🎯 Results:")
                print(f"   Voices downloaded: {summary.get('total_voices', 0)}")
                print(f"   Coverage level: {summary.get('coverage', 'unknown')}")
                print(f"   Status: {summary.get('status', 'unknown')}")
                
            except FileNotFoundError:
                print("⚠️ Summary file not found")
                
        else:
            print("❌ Enhanced downloader failed!")
            print(f"⏱️ Time taken: {elapsed:.1f} seconds")
            print("📋 Error output:")
            print(result.stderr)
            
    except subprocess.TimeoutExpired:
        print("⏰ Test timed out (10 minutes)")
    except Exception as e:
        print(f"💥 Test error: {e}")

if __name__ == "__main__":
    test_enhanced_downloader()
