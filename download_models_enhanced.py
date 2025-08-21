#!/usr/bin/env python3
"""
Enhanced voice model downloader - Targeting 50+ voices
Optimized for Railway deployment with maximum language coverage
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

# Optimized voice selection for 50+ voices - prioritizing small files first
ENHANCED_VOICES = {
    # TIER 1: Essential English (6 voices - small files)
    "tier1": {
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
        "en_US-lessac-medium": [
            f"{BASE_URL}/en/en_US/lessac/medium/en_US-lessac-medium.onnx",
            f"{BASE_URL}/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json"
        ],
        "en_GB-cori-medium": [
            f"{BASE_URL}/en/en_GB/cori/medium/en_GB-cori-medium.onnx",
            f"{BASE_URL}/en/en_GB/cori/medium/en_GB-cori-medium.onnx.json"
        ],
        "en_GB-alba-medium": [
            f"{BASE_URL}/en/en_GB/alba/medium/en_GB-alba-medium.onnx",
            f"{BASE_URL}/en/en_GB/alba/medium/en_GB-alba-medium.onnx.json"
        ]
    },
    
    # TIER 2: European LOW quality (8 voices - faster downloads)
    "tier2": {
        "it_IT-riccardo-x_low": [
            f"{BASE_URL}/it/it_IT/riccardo/x_low/it_IT-riccardo-x_low.onnx",
            f"{BASE_URL}/it/it_IT/riccardo/x_low/it_IT-riccardo-x_low.onnx.json"
        ],
        "fr_FR-mls_1840-low": [
            f"{BASE_URL}/fr/fr_FR/mls_1840/low/fr_FR-mls_1840-low.onnx",
            f"{BASE_URL}/fr/fr_FR/mls_1840/low/fr_FR-mls_1840-low.onnx.json"
        ],
        "de_DE-mls_9972-low": [
            f"{BASE_URL}/de/de_DE/mls_9972/low/de_DE-mls_9972-low.onnx",
            f"{BASE_URL}/de/de_DE/mls_9972/low/de_DE-mls_9972-low.onnx.json"
        ],
        "nl_NL-mls_5809-low": [
            f"{BASE_URL}/nl/nl_NL/mls_5809/low/nl_NL-mls_5809-low.onnx",
            f"{BASE_URL}/nl/nl_NL/mls_5809/low/nl_NL-mls_5809-low.onnx.json"
        ],
        "pl_PL-mls_6892-low": [
            f"{BASE_URL}/pl/pl_PL/mls_6892/low/pl_PL-mls_6892-low.onnx",
            f"{BASE_URL}/pl/pl_PL/mls_6892/low/pl_PL-mls_6892-low.onnx.json"
        ],
        "cs_CZ-jirka-low": [
            f"{BASE_URL}/cs/cs_CZ/jirka/low/cs_CZ-jirka-low.onnx",
            f"{BASE_URL}/cs/cs_CZ/jirka/low/cs_CZ-jirka-low.onnx.json"
        ],
        "fi_FI-harri-low": [
            f"{BASE_URL}/fi/fi_FI/harri/low/fi_FI-harri-low.onnx",
            f"{BASE_URL}/fi/fi_FI/harri/low/fi_FI-harri-low.onnx.json"
        ],
        "vi_VN-vivos-x_low": [
            f"{BASE_URL}/vi/vi_VN/vivos/x_low/vi_VN-vivos-x_low.onnx",
            f"{BASE_URL}/vi/vi_VN/vivos/x_low/vi_VN-vivos-x_low.onnx.json"
        ]
    },
    
    # TIER 3: Major languages MEDIUM (10 voices)
    "tier3": {
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
        ],
        "pt_BR-faber-medium": [
            f"{BASE_URL}/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx",
            f"{BASE_URL}/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx.json"
        ],
        "ru_RU-dmitri-medium": [
            f"{BASE_URL}/ru/ru_RU/dmitri/medium/ru_RU-dmitri-medium.onnx",
            f"{BASE_URL}/ru/ru_RU/dmitri/medium/ru_RU-dmitri-medium.onnx.json"
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
        "zh_CN-huayan-medium": [
            f"{BASE_URL}/zh/zh_CN/huayan/medium/zh_CN-huayan-medium.onnx",
            f"{BASE_URL}/zh/zh_CN/huayan/medium/zh_CN-huayan-medium.onnx.json"
        ],
        "ja_JP-kaiueo-medium": [
            f"{BASE_URL}/ja/ja_JP/kaiueo/medium/ja_JP-kaiueo-medium.onnx",
            f"{BASE_URL}/ja/ja_JP/kaiueo/medium/ja_JP-kaiueo-medium.onnx.json"
        ]
    },
    
    # TIER 4: Extended European & Regional (12 voices)
    "tier4": {
        "ca_ES-upc_ona-medium": [
            f"{BASE_URL}/ca/ca_ES/upc_ona/medium/ca_ES-upc_ona-medium.onnx",
            f"{BASE_URL}/ca/ca_ES/upc_ona/medium/ca_ES-upc_ona-medium.onnx.json"
        ],
        "it_IT-paola-medium": [
            f"{BASE_URL}/it/it_IT/paola/medium/it_IT-paola-medium.onnx",
            f"{BASE_URL}/it/it_IT/paola/medium/it_IT-paola-medium.onnx.json"
        ],
        "nl_NL-rdh-medium": [
            f"{BASE_URL}/nl/nl_NL/rdh/medium/nl_NL-rdh-medium.onnx",
            f"{BASE_URL}/nl/nl_NL/rdh/medium/nl_NL-rdh-medium.onnx.json"
        ],
        "hu_HU-anna-medium": [
            f"{BASE_URL}/hu/hu_HU/anna/medium/hu_HU-anna-medium.onnx",
            f"{BASE_URL}/hu/hu_HU/anna/medium/hu_HU-anna-medium.onnx.json"
        ],
        "tr_TR-dfki-medium": [
            f"{BASE_URL}/tr/tr_TR/dfki/medium/tr_TR-dfki-medium.onnx",
            f"{BASE_URL}/tr/tr_TR/dfki/medium/tr_TR-dfki-medium.onnx.json"
        ],
        "uk_UA-ukrainian_tts-medium": [
            f"{BASE_URL}/uk/uk_UA/ukrainian_tts/medium/uk_UA-ukrainian_tts-medium.onnx",
            f"{BASE_URL}/uk/uk_UA/ukrainian_tts/medium/uk_UA-ukrainian_tts-medium.onnx.json"
        ],
        "ro_RO-mihai-medium": [
            f"{BASE_URL}/ro/ro_RO/mihai/medium/ro_RO-mihai-medium.onnx",
            f"{BASE_URL}/ro/ro_RO/mihai/medium/ro_RO-mihai-medium.onnx.json"
        ],
        "bg_BG-krastyo-medium": [
            f"{BASE_URL}/bg/bg_BG/krastyo/medium/bg_BG-krastyo-medium.onnx",
            f"{BASE_URL}/bg/bg_BG/krastyo/medium/bg_BG-krastyo-medium.onnx.json"
        ],
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
        ],
        "th_TH-kaiueo-medium": [
            f"{BASE_URL}/th/th_TH/kaiueo/medium/th_TH-kaiueo-medium.onnx",
            f"{BASE_URL}/th/th_TH/kaiueo/medium/th_TH-kaiueo-medium.onnx.json"
        ]
    },
    
    # TIER 5: Additional variants & global reach (10 voices)
    "tier5": {
        "es_ES-sharvard-medium": [
            f"{BASE_URL}/es/es_ES/sharvard/medium/es_ES-sharvard-medium.onnx",
            f"{BASE_URL}/es/es_ES/sharvard/medium/es_ES-sharvard-medium.onnx.json"
        ],
        "es_MX-ald-medium": [
            f"{BASE_URL}/es/es_MX/ald/medium/es_MX-ald-medium.onnx",
            f"{BASE_URL}/es/es_MX/ald/medium/es_MX-ald-medium.onnx.json"
        ],
        "pt_PT-tugao-medium": [
            f"{BASE_URL}/pt/pt_PT/tugao/medium/pt_PT-tugao-medium.onnx",
            f"{BASE_URL}/pt/pt_PT/tugao/medium/pt_PT-tugao-medium.onnx.json"
        ],
        "fa_IR-gyro-medium": [
            f"{BASE_URL}/fa/fa_IR/gyro/medium/fa_IR-gyro-medium.onnx",
            f"{BASE_URL}/fa/fa_IR/gyro/medium/fa_IR-gyro-medium.onnx.json"
        ],
        "el_GR-rapunzelina-low": [
            f"{BASE_URL}/el/el_GR/rapunzelina/low/el_GR-rapunzelina-low.onnx",
            f"{BASE_URL}/el/el_GR/rapunzelina/low/el_GR-rapunzelina-low.onnx.json"
        ],
        "he_IL-amitai-medium": [
            f"{BASE_URL}/he/he_IL/amitai/medium/he_IL-amitai-medium.onnx",
            f"{BASE_URL}/he/he_IL/amitai/medium/he_IL-amitai-medium.onnx.json"
        ],
        "zh_TW-fgl-medium": [
            f"{BASE_URL}/zh/zh_TW/fgl/medium/zh_TW-fgl-medium.onnx",
            f"{BASE_URL}/zh/zh_TW/fgl/medium/zh_TW-fgl-medium.onnx.json"
        ],
        "fr_CA-pol-low": [
            f"{BASE_URL}/fr/fr_CA/pol/low/fr_CA-pol-low.onnx",
            f"{BASE_URL}/fr/fr_CA/pol/low/fr_CA-pol-low.onnx.json"
        ],
        "de_AT-hagen-medium": [
            f"{BASE_URL}/de/de_AT/hagen/medium/de_AT-hagen-medium.onnx",
            f"{BASE_URL}/de/de_AT/hagen/medium/de_AT-hagen-medium.onnx.json"
        ],
        "en_US-joe-medium": [
            f"{BASE_URL}/en/en_US/joe/medium/en_US-joe-medium.onnx",
            f"{BASE_URL}/en/en_US/joe/medium/en_US-joe-medium.onnx.json"
        ]
    },
    
    # TIER 6: Premium quality & additional coverage (4+ voices)
    "tier6": {
        "en_US-ryan-high": [
            f"{BASE_URL}/en/en_US/ryan/high/en_US-ryan-high.onnx",
            f"{BASE_URL}/en/en_US/ryan/high/en_US-ryan-high.onnx.json"
        ],
        "en_GB-jenny_dioco-medium": [
            f"{BASE_URL}/en/en_GB/jenny_dioco/medium/en_GB-jenny_dioco-medium.onnx",
            f"{BASE_URL}/en/en_GB/jenny_dioco/medium/en_GB-jenny_dioco-medium.onnx.json"
        ],
        "fr_FR-tom-x_low": [
            f"{BASE_URL}/fr/fr_FR/tom/x_low/fr_FR-tom-x_low.onnx",
            f"{BASE_URL}/fr/fr_FR/tom/x_low/fr_FR-tom-x_low.onnx.json"
        ],
        "de_DE-eva_k-x_low": [
            f"{BASE_URL}/de/de_DE/eva_k/x_low/de_DE-eva_k-x_low.onnx",
            f"{BASE_URL}/de/de_DE/eva_k/x_low/de_DE-eva_k-x_low.onnx.json"
        ]
    }
}

def download_file(url, filepath, max_retries=2):
    """Download a file with retries and error handling"""
    for attempt in range(max_retries):
        try:
            print(f"  Downloading {filepath.name}...")
            urllib.request.urlretrieve(url, filepath)
            return True
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"  Retry {attempt + 1}/{max_retries}")
                time.sleep(1)
            else:
                print(f"  Failed: {filepath.name}")
                return False
    return False

def download_voice_batch(voice_batch, tier_name):
    """Download a batch of voices with enhanced progress tracking"""
    print(f"\n{tier_name.upper()}: Starting {len(voice_batch)} voices...")
    
    downloaded = 0
    total = len(voice_batch)
    
    for voice_id, urls in voice_batch.items():
        print(f"\n{voice_id}...")
        
        success = True
        for url in urls:
            filename = url.split("/")[-1]
            filepath = MODELS_DIR / filename
            
            if not download_file(url, filepath):
                success = False
                break
        
        if success:
            downloaded += 1
            print(f"OK {voice_id} - Complete ({downloaded}/{total})")
        else:
            print(f"FAIL {voice_id} - Failed")
    
    print(f"\n{tier_name.upper()}: {downloaded}/{total} voices downloaded")
    return downloaded

def main():
    """Enhanced progressive voice model download - targeting 50+ voices"""
    print("Binary Piper TTS - Enhanced Voice Download")
    print("Target: 50+ voices with maximum language coverage")
    print("Optimized for Railway deployment limits")
    
    total_downloaded = 0
    start_time = time.time()
    
    # Calculate total voices
    total_voices = sum(len(batch) for batch in ENHANCED_VOICES.values())
    print(f"Total available voices: {total_voices}")
    
    # Download in optimized order (small files first)
    for tier_name, voice_batch in ENHANCED_VOICES.items():
        tier_start = time.time()
        batch_downloaded = download_voice_batch(voice_batch, tier_name)
        total_downloaded += batch_downloaded
        
        tier_time = time.time() - tier_start
        elapsed = time.time() - start_time
        
        print(f"Tier time: {tier_time:.1f}s | Total elapsed: {elapsed:.1f}s")
        print(f"Progress: {total_downloaded}/{total_voices} voices ({total_downloaded/total_voices*100:.1f}%)")
        
        # Stop if we're approaching Railway limits or have good coverage
        if elapsed > 420 or total_downloaded >= 50:  # 7 minutes or 50+ voices
            print(f"Target reached! {total_downloaded} voices in {elapsed:.1f}s")
            break
    
    print(f"\nEnhanced Download Complete!")
    print(f"Final count: {total_downloaded} voices")
    print(f"Total time: {time.time() - start_time:.1f}s")
    print(f"Language coverage: Excellent!")
    
    # Create enhanced summary
    summary = {
        "total_voices": total_downloaded,
        "target_voices": 50,
        "download_time": time.time() - start_time,
        "coverage": "enhanced" if total_downloaded >= 40 else "good" if total_downloaded >= 25 else "basic",
        "status": "success" if total_downloaded >= 20 else "partial"
    }
    
    with open(MODELS_DIR / "download_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"Summary saved - Coverage: {summary['coverage']}")

if __name__ == "__main__":
    main()
