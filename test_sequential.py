#!/usr/bin/env python3
"""
Test first 3 voices from sequential downloader
"""

import subprocess
import sys
import time

print("🧪 Testing Sequential Downloader (3 voices)")
print("=" * 50)

# Test with first 3 voices only
code = """
import sys
sys.path.append('.')
from download_models_sequential import OPTIMIZED_VOICES, download_voice_fast
from pathlib import Path

# Clean up
models_dir = Path("models")
models_dir.mkdir(exist_ok=True)

print("Testing first 3 voices...")
for i, voice_info in enumerate(OPTIMIZED_VOICES[:3]):
    print(f"Voice {i+1}: {voice_info[0]}")
    success = download_voice_fast(voice_info) 
    if success:
        print(f"✓ Success: {voice_info[0]}")
    else:
        print(f"✗ Failed: {voice_info[0]}")

print("Test complete")
"""

try:
    start = time.time()
    result = subprocess.run([sys.executable, "-c", code], 
                          capture_output=True, text=True, timeout=180)
    elapsed = time.time() - start
    
    print(f"Result in {elapsed:.1f}s:")
    print("STDOUT:", result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
        
except Exception as e:
    print(f"Error: {e}")
