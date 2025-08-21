#!/usr/bin/env python3
"""
Sequential Ultra-Optimized voice downloader - Targeting 50+ voices
Maximum efficiency with reliable sequential downloads
"""
import os
import urllib.request
import urllib.error
from pathlib import Path
import json
import time
import sys

MODELS_DIR = Path("models")
MODELS_DIR.mkdir(exist_ok=True)

BASE_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/main"

# Optimized voice selection - 52 voices prioritized by size and importance
OPTIMIZED_VOICES = [
    # Tier 1: Essential small files (12 voices)
    ("en_US-amy-low", "en", "US", "low"),
    ("en_US-danny-low", "en", "US", "low"), 
    ("en_US-kathleen-low", "en", "US", "low"),
    ("it_IT-riccardo-x_low", "it", "IT", "x_low"),
    ("vi_VN-vivos-x_low", "vi", "VN", "x_low"),
    ("fr_FR-tom-x_low", "fr", "FR", "x_low"),
    ("de_DE-eva_k-x_low", "de", "DE", "x_low"),
    ("fr_FR-mls_1840-low", "fr", "FR", "low"),
    ("de_DE-mls_9972-low", "de", "DE", "low"),
    ("nl_NL-mls_5809-low", "nl", "NL", "low"),
    ("pl_PL-mls_6892-low", "pl", "PL", "low"),
    ("cs_CZ-jirka-low", "cs", "CZ", "low"),
    
    # Tier 2: Essential medium files (12 voices)  
    ("en_US-lessac-medium", "en", "US", "medium"),
    ("en_GB-cori-medium", "en", "GB", "medium"),
    ("es_ES-davefx-medium", "es", "ES", "medium"),
    ("fr_FR-siwis-medium", "fr", "FR", "medium"),
    ("de_DE-thorsten-medium", "de", "DE", "medium"),
    ("pt_BR-faber-medium", "pt", "BR", "medium"),
    ("ru_RU-dmitri-medium", "ru", "RU", "medium"),
    ("zh_CN-huayan-medium", "zh", "CN", "medium"),
    ("ja_JP-kaiueo-medium", "ja", "JP", "medium"),
    ("sv_SE-nst-medium", "sv", "SE", "medium"),
    ("da_DK-talesyntese-medium", "da", "DK", "medium"),
    ("no_NO-talesyntese-medium", "no", "NO", "medium"),
    
    # Tier 3: Regional coverage (10 voices)
    ("fi_FI-harri-low", "fi", "FI", "low"),
    ("ca_ES-upc_ona-medium", "ca", "ES", "medium"), 
    ("it_IT-paola-medium", "it", "IT", "medium"),
    ("hu_HU-anna-medium", "hu", "HU", "medium"),
    ("ar_JO-kareem-medium", "ar", "JO", "medium"),
    ("hi_IN-male-medium", "hi", "IN", "medium"),
    ("ko_KR-kss-medium", "ko", "KR", "medium"),
    ("th_TH-kaiueo-medium", "th", "TH", "medium"),
    ("tr_TR-dfki-medium", "tr", "TR", "medium"),
    ("uk_UA-ukrainian_tts-medium", "uk", "UA", "medium"),
    
    # Tier 4: Extended variants (8 voices)
    ("en_GB-alba-medium", "en", "GB", "medium"),
    ("es_ES-sharvard-medium", "es", "ES", "medium"),
    ("nl_NL-rdh-medium", "nl", "NL", "medium"),
    ("ro_RO-mihai-medium", "ro", "RO", "medium"),
    ("bg_BG-krastyo-medium", "bg", "BG", "medium"),
    ("fa_IR-gyro-medium", "fa", "IR", "medium"),
    ("el_GR-rapunzelina-low", "el", "GR", "low"),
    ("he_IL-amitai-medium", "he", "IL", "medium"),
    
    # Tier 5: Additional variants (10+ voices)
    ("en_US-joe-medium", "en", "US", "medium"),
    ("es_MX-ald-medium", "es", "MX", "medium"), 
    ("pt_PT-tugao-medium", "pt", "PT", "medium"),
    ("fr_CA-pol-low", "fr", "CA", "low"),
    ("de_AT-hagen-medium", "de", "AT", "medium"),
    ("zh_TW-fgl-medium", "zh", "TW", "medium"),
    ("sl_SI-artur-medium", "sl", "SI", "medium"),
    ("sk_SK-lili-medium", "sk", "SK", "medium"),
    ("en_US-ryan-high", "en", "US", "high"),
    ("en_GB-jenny_dioco-medium", "en", "GB", "medium")
]

def build_urls(voice_id, lang, country, quality):
    """Build URLs for a voice"""
    # Extract speaker name from voice_id (format: lang_country-speaker-quality)
    parts = voice_id.split('-')
    if len(parts) >= 3:
        speaker = parts[1]
    else:
        speaker = parts[-2] if len(parts) > 1 else "default"
    
    voice_path = f"{lang}/{lang}_{country}/{speaker}/{quality}"
    return [
        f"{BASE_URL}/{voice_path}/{voice_id}.onnx",
        f"{BASE_URL}/{voice_path}/{voice_id}.onnx.json"
    ]

def download_file_fast(url, filepath, timeout=60):
    """Download a single file with optimized settings"""
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        
        with urllib.request.urlopen(req, timeout=timeout) as response:
            with open(filepath, 'wb') as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f"    Error: {e}")
        return False

def download_voice_fast(voice_info):
    """Download a voice quickly"""
    voice_id, lang, country, quality = voice_info
    print(f"  {voice_id}...")
    
    urls = build_urls(voice_id, lang, country, quality)
    
    for url in urls:
        filename = url.split("/")[-1]
        filepath = MODELS_DIR / filename
        
        if not download_file_fast(url, filepath):
            return False
            
    print(f"  ✓ {voice_id}")
    return True

def main():
    """Ultra-optimized sequential download targeting 50+ voices"""
    print("Binary Piper TTS - Sequential Ultra-Optimized Download")
    print("Target: 50+ voices with maximum reliability")
    
    total_downloaded = 0
    start_time = time.time()
    
    print(f"Total voices to download: {len(OPTIMIZED_VOICES)}")
    
    # Time checkpoints for Railway limits
    checkpoints = [120, 240, 360, 480]  # 2, 4, 6, 8 minute marks
    checkpoint_targets = [15, 30, 42, 52]  # Target voices by each checkpoint
    
    for i, voice_info in enumerate(OPTIMIZED_VOICES):
        elapsed = time.time() - start_time
        
        # Check if we should stop due to time constraints
        if elapsed > 450:  # 7.5 minutes hard limit
            print(f"Time limit reached at {elapsed:.1f}s")
            break
            
        # Progress updates at checkpoints
        for checkpoint, target in zip(checkpoints, checkpoint_targets):
            if elapsed > checkpoint and total_downloaded < target:
                print(f"Behind schedule at {checkpoint}s: {total_downloaded}/{target}")
                break
        
        print(f"\n[{i+1}/{len(OPTIMIZED_VOICES)}] Downloading...")
        
        if download_voice_fast(voice_info):
            total_downloaded += 1
            print(f"  SUCCESS: {voice_info[0]} ({total_downloaded})")
        else:
            print(f"  FAILED: {voice_info[0]}")
        # Quick progress update
        if total_downloaded % 5 == 0:
            progress_pct = (total_downloaded / len(OPTIMIZED_VOICES)) * 100
            print(f"Progress: {total_downloaded} voices ({progress_pct:.1f}%) in {elapsed:.1f}s")
        
        # Stop if we achieve target early
        if total_downloaded >= 52:
            print(f"Target exceeded! {total_downloaded} voices achieved")
            break
        
        # Brief pause to avoid overwhelming servers
        if i % 10 == 9:  # Every 10 downloads
            time.sleep(1)
    
    elapsed = time.time() - start_time
    
    print(f"\nSequential Ultra-Optimized Download Complete!")
    print(f"Final count: {total_downloaded} voices") 
    print(f"Total time: {elapsed:.1f}s")
    print(f"Average: {elapsed/total_downloaded:.1f}s per voice")
    
    # Enhanced summary
    summary = {
        "total_voices": total_downloaded,
        "target_voices": 50,
        "download_time": elapsed,
        "voices_per_minute": total_downloaded / (elapsed / 60),
        "coverage": "ultra" if total_downloaded >= 50 else "enhanced" if total_downloaded >= 40 else "good",
        "status": "ultra-success" if total_downloaded >= 50 else "success"
    }
    
    with open(MODELS_DIR / "download_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"Rate: {summary['voices_per_minute']:.1f} voices/min")
    
    if total_downloaded >= 50:
        print("🎯 ULTRA SUCCESS: 50+ voice target achieved!")
    elif total_downloaded >= 45:
        print("✨ NEAR TARGET: Very close to 50 voice goal!")
    else:
        print("📈 PROGRESS: Significant improvement!")

if __name__ == "__main__":
    main()
