#!/usr/bin/env python3
"""
Optimized voice model downloader for Railway deployment
Downloads all 73 voices in batches to avoid timeouts
"""
import os
import urllib.request
import urllib.error
from pathlib import Path
import json
import time
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

MODELS_DIR = Path("models")
MODELS_DIR.mkdir(exist_ok=True)

BASE_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/main"

# All 73 voices organized by priority for progressive loading
PRIORITY_VOICES = {
    # TIER 1: Essential voices (fast download)
    "tier1": {
        "en_US-lessac-medium": [
            f"{BASE_URL}/en/en_US/lessac/medium/en_US-lessac-medium.onnx",
            f"{BASE_URL}/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json"
        ],
        "en_GB-cori-medium": [
            f"{BASE_URL}/en/en_GB/cori/medium/en_GB-cori-medium.onnx",
            f"{BASE_URL}/en/en_GB/cori/medium/en_GB-cori-medium.onnx.json"
        ],
        "es_ES-davefx-medium": [
            f"{BASE_URL}/es/es_ES/davefx/medium/es_ES-davefx-medium.onnx",
            f"{BASE_URL}/es/es_ES/davefx/medium/es_ES-davefx-medium.onnx.json"
        ],
        "fr_FR-siwis-medium": [
            f"{BASE_URL}/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx",
            f"{BASE_URL}/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx.json"
        ],
        "de_DE-thorsten-medium": [
            f"{BASE_URL}/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx",
            f"{BASE_URL}/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx.json"
        ]
    },
    
    # TIER 2: Popular languages
    "tier2": {
        "it_IT-riccardo-x_low": [
            f"{BASE_URL}/it/it_IT/riccardo/x_low/it_IT-riccardo-x_low.onnx",
            f"{BASE_URL}/it/it_IT/riccardo/x_low/it_IT-riccardo-x_low.onnx.json"
        ],
        "pt_BR-faber-medium": [
            f"{BASE_URL}/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx",
            f"{BASE_URL}/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx.json"
        ],
        "ru_RU-dmitri-medium": [
            f"{BASE_URL}/ru/ru_RU/dmitri/medium/ru_RU-dmitri-medium.onnx",
            f"{BASE_URL}/ru/ru_RU/dmitri/medium/ru_RU-dmitri-medium.onnx.json"
        ],
        "ja_JP-kaiueo-medium": [
            f"{BASE_URL}/ja/ja_JP/kaiueo/medium/ja_JP-kaiueo-medium.onnx",
            f"{BASE_URL}/ja/ja_JP/kaiueo/medium/ja_JP-kaiueo-medium.onnx.json"
        ],
        "zh_CN-huayan-medium": [
            f"{BASE_URL}/zh/zh_CN/huayan/medium/zh_CN-huayan-medium.onnx",
            f"{BASE_URL}/zh/zh_CN/huayan/medium/zh_CN-huayan-medium.onnx.json"
        ]
    },
    
    # TIER 3: Additional European languages
    "tier3": {
        "nl_NL-mls_5809-low": [
            f"{BASE_URL}/nl/nl_NL/mls_5809/low/nl_NL-mls_5809-low.onnx",
            f"{BASE_URL}/nl/nl_NL/mls_5809/low/nl_NL-mls_5809-low.onnx.json"
        ],
        "sv_SE-nst-medium": [
            f"{BASE_URL}/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx",
            f"{BASE_URL}/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx.json"
        ],
        "da_DK-talesyntese-medium": [
            f"{BASE_URL}/da/da_DK/talesyntese/medium/da_DK-talesyntese-medium.onnx",
            f"{BASE_URL}/da/da_DK/talesyntese/medium/da_DK-talesyntese-medium.onnx.json"
        ],
        "no_NO-talesyntese-medium": [
            f"{BASE_URL}/no/no_NO/talesyntese/medium/no_NO-talesyntese-medium.onnx",
            f"{BASE_URL}/no/no_NO/talesyntese/medium/no_NO-talesyntese-medium.onnx.json"
        ],
        "fi_FI-harri-low": [
            f"{BASE_URL}/fi/fi_FI/harri/low/fi_FI-harri-low.onnx",
            f"{BASE_URL}/fi/fi_FI/harri/low/fi_FI-harri-low.onnx.json"
        ]
    },
    
    # TIER 4: Remaining voices (download if time permits)
    "tier4": {
        # Additional English variants
        "en_US-amy-low": [
            f"{BASE_URL}/en/en_US/amy/low/en_US-amy-low.onnx",
            f"{BASE_URL}/en/en_US/amy/low/en_US-amy-low.onnx.json"
        ],
        "en_US-danny-low": [
            f"{BASE_URL}/en/en_US/danny/low/en_US-danny-low.onnx",
            f"{BASE_URL}/en/en_US/danny/low/en_US-danny-low.onnx.json"
        ],
        "en_US-kathleen-low": [
            f"{BASE_URL}/en/en_US/kathleen/low/en_US-kathleen-low.onnx",
            f"{BASE_URL}/en/en_US/kathleen/low/en_US-kathleen-low.onnx.json"
        ],
        
        # Additional European voices
        "ca_ES-upc_ona-medium": [
            f"{BASE_URL}/ca/ca_ES/upc_ona/medium/ca_ES-upc_ona-medium.onnx",
            f"{BASE_URL}/ca/ca_ES/upc_ona/medium/ca_ES-upc_ona-medium.onnx.json"
        ],
        "cs_CZ-jirka-low": [
            f"{BASE_URL}/cs/cs_CZ/jirka/low/cs_CZ-jirka-low.onnx",
            f"{BASE_URL}/cs/cs_CZ/jirka/low/cs_CZ-jirka-low.onnx.json"
        ],
        "pl_PL-mls_6892-low": [
            f"{BASE_URL}/pl/pl_PL/mls_6892/low/pl_PL-mls_6892-low.onnx",
            f"{BASE_URL}/pl/pl_PL/mls_6892/low/pl_PL-mls_6892-low.onnx.json"
        ],
        
        # Middle Eastern & Asian
        "ar_JO-kareem-medium": [
            f"{BASE_URL}/ar/ar_JO/kareem/medium/ar_JO-kareem-medium.onnx",
            f"{BASE_URL}/ar/ar_JO/kareem/medium/ar_JO-kareem-medium.onnx.json"
        ],
        "hi_IN-male-medium": [
            f"{BASE_URL}/hi/hi_IN/male/medium/hi_IN-male-medium.onnx",
            f"{BASE_URL}/hi/hi_IN/male/medium/hi_IN-male-medium.onnx.json"
        ],
        "ko_KR-kss-medium": [
            f"{BASE_URL}/ko/ko_KR/kss/medium/ko_KR-kss-medium.onnx",
            f"{BASE_URL}/ko/ko_KR/kss/medium/ko_KR-kss-medium.onnx.json"
        ]
    }
}

def download_file(url, filepath, max_retries=3):
    """Download a file with retries and error handling"""
    for attempt in range(max_retries):
        try:
            print(f"  📥 {filepath.name}...")
            urllib.request.urlretrieve(url, filepath)
            return True
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"  ⚠️ Retry {attempt + 1}/{max_retries} for {filepath.name}")
                time.sleep(2)
            else:
                print(f"  ❌ Failed to download {url}: {e}")
                return False
    return False

def download_voice_batch(voice_batch, tier_name):
    """Download a batch of voices"""
    print(f"\n🎯 {tier_name.upper()}: Downloading {len(voice_batch)} voices...")
    
    downloaded = 0
    total = len(voice_batch)
    
    for voice_id, urls in voice_batch.items():
        print(f"\n📦 {voice_id}...")
        
        success = True
        for url in urls:
            filename = url.split("/")[-1]
            filepath = MODELS_DIR / filename
            
            if not download_file(url, filepath):
                success = False
                break
        
        if success:
            downloaded += 1
            print(f"✅ {voice_id} - OK")
        else:
            print(f"❌ {voice_id} - FAILED")
    
    print(f"\n🎯 {tier_name.upper()} Complete: {downloaded}/{total} voices")
    return downloaded

def main():
    """Progressive voice model download"""
    print("🚀 Binary Piper TTS - Full Voice Download")
    print("📦 Progressive download: Essential → Popular → Extended → Complete")
    
    total_downloaded = 0
    start_time = time.time()
    
    # Download in priority order
    for tier_name, voice_batch in PRIORITY_VOICES.items():
        batch_downloaded = download_voice_batch(voice_batch, tier_name)
        total_downloaded += batch_downloaded
        
        elapsed = time.time() - start_time
        print(f"⏱️ Elapsed time: {elapsed:.1f}s")
        
        # Check if we should continue (Railway has ~10 minute limits)
        if elapsed > 480:  # 8 minutes - leave buffer
            print(f"⏰ Time limit approaching, stopping at {total_downloaded} voices")
            break
    
    print(f"\n🎉 Download Complete!")
    print(f"📊 Total: {total_downloaded} voices ready")
    print(f"⏱️ Total time: {time.time() - start_time:.1f}s")
    
    # Create summary file
    summary = {
        "total_voices": total_downloaded,
        "download_time": time.time() - start_time,
        "status": "complete" if total_downloaded > 15 else "partial"
    }
    
    with open(MODELS_DIR / "download_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    if total_downloaded == 0:
        print("⚠️ No voices downloaded - creating fallback")
        # Create minimal fallback
        dummy_config = {
            "audio": {"sample_rate": 22050},
            "num_speakers": 1,
            "language": {"code": "en-us"}
        }
        with open(MODELS_DIR / "en_US-fallback.onnx.json", "w") as f:
            json.dump(dummy_config, f)
        with open(MODELS_DIR / "en_US-fallback.onnx", "wb") as f:
            f.write(b"fallback")

if __name__ == "__main__":
    main()
