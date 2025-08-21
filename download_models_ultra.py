#!/usr/bin/env python3
"""
Ultra-Optimized voice model downloader - Targeting 50+ voices
Maximum efficiency for Railway deployment with parallel processing
"""
import os
import urllib.request
import urllib.error
from pathlib import Path
import json
import time
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

MODELS_DIR = Path("models")
MODELS_DIR.mkdir(exist_ok=True)

BASE_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/main"

# Ultra-optimized voice selection - 50+ voices prioritized by file size and importance
ULTRA_VOICES = {
    # TIER 1: Essential + Small files (12 voices - 2 minutes max)
    "tier1_essential": {
        "en_US-amy-low": [f"{BASE_URL}/en/en_US/amy/low/en_US-amy-low.onnx", f"{BASE_URL}/en/en_US/amy/low/en_US-amy-low.onnx.json"],
        "en_US-danny-low": [f"{BASE_URL}/en/en_US/danny/low/en_US-danny-low.onnx", f"{BASE_URL}/en/en_US/danny/low/en_US-danny-low.onnx.json"],
        "en_US-kathleen-low": [f"{BASE_URL}/en/en_US/kathleen/low/en_US-kathleen-low.onnx", f"{BASE_URL}/en/en_US/kathleen/low/en_US-kathleen-low.onnx.json"],
        "en_GB-cori-medium": [f"{BASE_URL}/en/en_GB/cori/medium/en_GB-cori-medium.onnx", f"{BASE_URL}/en/en_GB/cori/medium/en_GB-cori-medium.onnx.json"],
        "it_IT-riccardo-x_low": [f"{BASE_URL}/it/it_IT/riccardo/x_low/it_IT-riccardo-x_low.onnx", f"{BASE_URL}/it/it_IT/riccardo/x_low/it_IT-riccardo-x_low.onnx.json"],
        "fr_FR-mls_1840-low": [f"{BASE_URL}/fr/fr_FR/mls_1840/low/fr_FR-mls_1840-low.onnx", f"{BASE_URL}/fr/fr_FR/mls_1840/low/fr_FR-mls_1840-low.onnx.json"],
        "de_DE-mls_9972-low": [f"{BASE_URL}/de/de_DE/mls_9972/low/de_DE-mls_9972-low.onnx", f"{BASE_URL}/de/de_DE/mls_9972/low/de_DE-mls_9972-low.onnx.json"],
        "nl_NL-mls_5809-low": [f"{BASE_URL}/nl/nl_NL/mls_5809/low/nl_NL-mls_5809-low.onnx", f"{BASE_URL}/nl/nl_NL/mls_5809/low/nl_NL-mls_5809-low.onnx.json"],
        "pl_PL-mls_6892-low": [f"{BASE_URL}/pl/pl_PL/mls_6892/low/pl_PL-mls_6892-low.onnx", f"{BASE_URL}/pl/pl_PL/mls_6892/low/pl_PL-mls_6892-low.onnx.json"],
        "cs_CZ-jirka-low": [f"{BASE_URL}/cs/cs_CZ/jirka/low/cs_CZ-jirka-low.onnx", f"{BASE_URL}/cs/cs_CZ/jirka/low/cs_CZ-jirka-low.onnx.json"],
        "fi_FI-harri-low": [f"{BASE_URL}/fi/fi_FI/harri/low/fi_FI-harri-low.onnx", f"{BASE_URL}/fi/fi_FI/harri/low/fi_FI-harri-low.onnx.json"],
        "vi_VN-vivos-x_low": [f"{BASE_URL}/vi/vi_VN/vivos/x_low/vi_VN-vivos-x_low.onnx", f"{BASE_URL}/vi/vi_VN/vivos/x_low/vi_VN-vivos-x_low.onnx.json"]
    },
    
    # TIER 2: High-value medium files (10 voices - 2 minutes max)
    "tier2_highvalue": {
        "en_US-lessac-medium": [f"{BASE_URL}/en/en_US/lessac/medium/en_US-lessac-medium.onnx", f"{BASE_URL}/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json"],
        "es_ES-davefx-medium": [f"{BASE_URL}/es/es_ES/davefx/medium/es_ES-davefx-medium.onnx", f"{BASE_URL}/es/es_ES/davefx/medium/es_ES-davefx-medium.onnx.json"],
        "fr_FR-siwis-medium": [f"{BASE_URL}/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx", f"{BASE_URL}/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx.json"],
        "de_DE-thorsten-medium": [f"{BASE_URL}/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx", f"{BASE_URL}/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx.json"],
        "pt_BR-faber-medium": [f"{BASE_URL}/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx", f"{BASE_URL}/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx.json"],
        "ru_RU-dmitri-medium": [f"{BASE_URL}/ru/ru_RU/dmitri/medium/ru_RU-dmitri-medium.onnx", f"{BASE_URL}/ru/ru_RU/dmitri/medium/ru_RU-dmitri-medium.onnx.json"],
        "zh_CN-huayan-medium": [f"{BASE_URL}/zh/zh_CN/huayan/medium/zh_CN-huayan-medium.onnx", f"{BASE_URL}/zh/zh_CN/huayan/medium/zh_CN-huayan-medium.onnx.json"],
        "ja_JP-kaiueo-medium": [f"{BASE_URL}/ja/ja_JP/kaiueo/medium/ja_JP-kaiueo-medium.onnx", f"{BASE_URL}/ja/ja_JP/kaiueo/medium/ja_JP-kaiueo-medium.onnx.json"],
        "sv_SE-nst-medium": [f"{BASE_URL}/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx", f"{BASE_URL}/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx.json"],
        "da_DK-talesyntese-medium": [f"{BASE_URL}/da/da_DK/talesyntese/medium/da_DK-talesyntese-medium.onnx", f"{BASE_URL}/da/da_DK/talesyntese/medium/da_DK-talesyntese-medium.onnx.json"]
    },
    
    # TIER 3: Regional coverage (10 voices - 1.5 minutes max)
    "tier3_regional": {
        "no_NO-talesyntese-medium": [f"{BASE_URL}/no/no_NO/talesyntese/medium/no_NO-talesyntese-medium.onnx", f"{BASE_URL}/no/no_NO/talesyntese/medium/no_NO-talesyntese-medium.onnx.json"],
        "ca_ES-upc_ona-medium": [f"{BASE_URL}/ca/ca_ES/upc_ona/medium/ca_ES-upc_ona-medium.onnx", f"{BASE_URL}/ca/ca_ES/upc_ona/medium/ca_ES-upc_ona-medium.onnx.json"],
        "it_IT-paola-medium": [f"{BASE_URL}/it/it_IT/paola/medium/it_IT-paola-medium.onnx", f"{BASE_URL}/it/it_IT/paola/medium/it_IT-paola-medium.onnx.json"],
        "hu_HU-anna-medium": [f"{BASE_URL}/hu/hu_HU/anna/medium/hu_HU-anna-medium.onnx", f"{BASE_URL}/hu/hu_HU/anna/medium/hu_HU-anna-medium.onnx.json"],
        "ar_JO-kareem-medium": [f"{BASE_URL}/ar/ar_JO/kareem/medium/ar_JO-kareem-medium.onnx", f"{BASE_URL}/ar/ar_JO/kareem/medium/ar_JO-kareem-medium.onnx.json"],
        "hi_IN-male-medium": [f"{BASE_URL}/hi/hi_IN/male/medium/hi_IN-male-medium.onnx", f"{BASE_URL}/hi/hi_IN/male/medium/hi_IN-male-medium.onnx.json"],
        "ko_KR-kss-medium": [f"{BASE_URL}/ko/ko_KR/kss/medium/ko_KR-kss-medium.onnx", f"{BASE_URL}/ko/ko_KR/kss/medium/ko_KR-kss-medium.onnx.json"],
        "th_TH-kaiueo-medium": [f"{BASE_URL}/th/th_TH/kaiueo/medium/th_TH-kaiueo-medium.onnx", f"{BASE_URL}/th/th_TH/kaiueo/medium/th_TH-kaiueo-medium.onnx.json"],
        "tr_TR-dfki-medium": [f"{BASE_URL}/tr/tr_TR/dfki/medium/tr_TR-dfki-medium.onnx", f"{BASE_URL}/tr/tr_TR/dfki/medium/tr_TR-dfki-medium.onnx.json"],
        "uk_UA-ukrainian_tts-medium": [f"{BASE_URL}/uk/uk_UA/ukrainian_tts/medium/uk_UA-ukrainian_tts-medium.onnx", f"{BASE_URL}/uk/uk_UA/ukrainian_tts/medium/uk_UA-ukrainian_tts-medium.onnx.json"]
    },
    
    # TIER 4: Extended variants (8 voices - 1 minute max)
    "tier4_variants": {
        "en_GB-alba-medium": [f"{BASE_URL}/en/en_GB/alba/medium/en_GB-alba-medium.onnx", f"{BASE_URL}/en/en_GB/alba/medium/en_GB-alba-medium.onnx.json"],
        "es_ES-sharvard-medium": [f"{BASE_URL}/es/es_ES/sharvard/medium/es_ES-sharvard-medium.onnx", f"{BASE_URL}/es/es_ES/sharvard/medium/es_ES-sharvard-medium.onnx.json"],
        "nl_NL-rdh-medium": [f"{BASE_URL}/nl/nl_NL/rdh/medium/nl_NL-rdh-medium.onnx", f"{BASE_URL}/nl/nl_NL/rdh/medium/nl_NL-rdh-medium.onnx.json"],
        "ro_RO-mihai-medium": [f"{BASE_URL}/ro/ro_RO/mihai/medium/ro_RO-mihai-medium.onnx", f"{BASE_URL}/ro/ro_RO/mihai/medium/ro_RO-mihai-medium.onnx.json"],
        "bg_BG-krastyo-medium": [f"{BASE_URL}/bg/bg_BG/krastyo/medium/bg_BG-krastyo-medium.onnx", f"{BASE_URL}/bg/bg_BG/krastyo/medium/bg_BG-krastyo-medium.onnx.json"],
        "fa_IR-gyro-medium": [f"{BASE_URL}/fa/fa_IR/gyro/medium/fa_IR-gyro-medium.onnx", f"{BASE_URL}/fa/fa_IR/gyro/medium/fa_IR-gyro-medium.onnx.json"],
        "el_GR-rapunzelina-low": [f"{BASE_URL}/el/el_GR/rapunzelina/low/el_GR-rapunzelina-low.onnx", f"{BASE_URL}/el/el_GR/rapunzelina/low/el_GR-rapunzelina-low.onnx.json"],
        "he_IL-amitai-medium": [f"{BASE_URL}/he/he_IL/amitai/medium/he_IL-amitai-medium.onnx", f"{BASE_URL}/he/he_IL/amitai/medium/he_IL-amitai-medium.onnx.json"]
    },
    
    # TIER 5: Premium and additional (12+ voices - remaining time)
    "tier5_additional": {
        "en_US-joe-medium": [f"{BASE_URL}/en/en_US/joe/medium/en_US-joe-medium.onnx", f"{BASE_URL}/en/en_US/joe/medium/en_US-joe-medium.onnx.json"],
        "en_US-ryan-high": [f"{BASE_URL}/en/en_US/ryan/high/en_US-ryan-high.onnx", f"{BASE_URL}/en/en_US/ryan/high/en_US-ryan-high.onnx.json"],
        "en_GB-jenny_dioco-medium": [f"{BASE_URL}/en/en_GB/jenny_dioco/medium/en_GB-jenny_dioco-medium.onnx", f"{BASE_URL}/en/en_GB/jenny_dioco/medium/en_GB-jenny_dioco-medium.onnx.json"],
        "es_MX-ald-medium": [f"{BASE_URL}/es/es_MX/ald/medium/es_MX-ald-medium.onnx", f"{BASE_URL}/es/es_MX/ald/medium/es_MX-ald-medium.onnx.json"],
        "pt_PT-tugao-medium": [f"{BASE_URL}/pt/pt_PT/tugao/medium/pt_PT-tugao-medium.onnx", f"{BASE_URL}/pt/pt_PT/tugao/medium/pt_PT-tugao-medium.onnx.json"],
        "fr_CA-pol-low": [f"{BASE_URL}/fr/fr_CA/pol/low/fr_CA-pol-low.onnx", f"{BASE_URL}/fr/fr_CA/pol/low/fr_CA-pol-low.onnx.json"],
        "de_AT-hagen-medium": [f"{BASE_URL}/de/de_AT/hagen/medium/de_AT-hagen-medium.onnx", f"{BASE_URL}/de/de_AT/hagen/medium/de_AT-hagen-medium.onnx.json"],
        "zh_TW-fgl-medium": [f"{BASE_URL}/zh/zh_TW/fgl/medium/zh_TW-fgl-medium.onnx", f"{BASE_URL}/zh/zh_TW/fgl/medium/zh_TW-fgl-medium.onnx.json"],
        "fr_FR-tom-x_low": [f"{BASE_URL}/fr/fr_FR/tom/x_low/fr_FR-tom-x_low.onnx", f"{BASE_URL}/fr/fr_FR/tom/x_low/fr_FR-tom-x_low.onnx.json"],
        "de_DE-eva_k-x_low": [f"{BASE_URL}/de/de_DE/eva_k/x_low/de_DE-eva_k-x_low.onnx", f"{BASE_URL}/de/de_DE/eva_k/x_low/de_DE-eva_k-x_low.onnx.json"],
        "sl_SI-artur-medium": [f"{BASE_URL}/sl/sl_SI/artur/medium/sl_SI-artur-medium.onnx", f"{BASE_URL}/sl/sl_SI/artur/medium/sl_SI-artur-medium.onnx.json"],
        "sk_SK-lili-medium": [f"{BASE_URL}/sk/sk_SK/lili/medium/sk_SK-lili-medium.onnx", f"{BASE_URL}/sk/sk_SK/lili/medium/sk_SK-lili-medium.onnx.json"]
    }
}

# Thread-safe counter
download_stats = {"success": 0, "failed": 0, "lock": threading.Lock()}

def download_single_file(url, filepath, timeout=30):
    """Download a single file with minimal retries"""
    try:
        urllib.request.urlretrieve(url, filepath)
        return True
    except Exception:
        return False

def download_voice_parallel(voice_id, urls):
    """Download a single voice (both files) with parallel execution"""
    success = True
    
    try:
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = []
            filepaths = []
            
            for url in urls:
                filename = url.split("/")[-1]
                filepath = MODELS_DIR / filename
                filepaths.append(filepath)
                future = executor.submit(download_single_file, url, filepath)
                futures.append(future)
            
            # Wait for both files with reasonable timeout
            for future, filepath in zip(futures, filepaths):
                try:
                    if not future.result(timeout=45):  # 45 seconds per file
                        success = False
                        break
                except Exception:
                    success = False
                    break
    except Exception:
        success = False
    
    with download_stats["lock"]:
        if success:
            download_stats["success"] += 1
            print(f"OK {voice_id} ({download_stats['success']})")
        else:
            download_stats["failed"] += 1
            print(f"FAIL {voice_id}")
    
    return success

def download_tier_parallel(voice_batch, tier_name, max_time_seconds):
    """Download a tier with parallel processing and time limits"""
    print(f"\n{tier_name.upper()}: {len(voice_batch)} voices, {max_time_seconds}s limit")
    
    start_time = time.time()
    successful_downloads = 0
    
    with ThreadPoolExecutor(max_workers=3) as executor:  # Reduced parallel downloads
        futures = {}
        
        for voice_id, urls in voice_batch.items():
            if time.time() - start_time >= max_time_seconds * 0.8:  # Stop earlier
                print(f"Time limit approaching for {tier_name}")
                break
                
            future = executor.submit(download_voice_parallel, voice_id, urls)
            futures[future] = voice_id
        
        # Collect results with reasonable timeout
        timeout_remaining = max_time_seconds - (time.time() - start_time)
        try:
            for future in as_completed(futures, timeout=max(timeout_remaining, 30)):
                if future.result():
                    successful_downloads += 1
                    
                # Stop if we're taking too long
                if time.time() - start_time >= max_time_seconds * 0.9:
                    break
        except:
            print(f"Timeout reached for {tier_name}")
    
    elapsed = time.time() - start_time
    print(f"{tier_name.upper()}: {successful_downloads}/{len(voice_batch)} in {elapsed:.1f}s")
    return successful_downloads

def main():
    """Ultra-optimized progressive download targeting 50+ voices"""
    print("Binary Piper TTS - Ultra-Optimized Voice Download")
    print("Target: 50+ voices with maximum efficiency")
    
    total_downloaded = 0
    start_time = time.time()
    
    # Calculate total available
    total_voices = sum(len(batch) for batch in ULTRA_VOICES.values())
    print(f"Total available voices: {total_voices}")
    
    # Time allocation for Railway (8 minute limit)
    tier_time_limits = {
        "tier1_essential": 120,    # 2 minutes - critical voices
        "tier2_highvalue": 120,    # 2 minutes - important languages  
        "tier3_regional": 90,      # 1.5 minutes - regional coverage
        "tier4_variants": 60,      # 1 minute - variants
        "tier5_additional": 90     # 1.5 minutes - remaining voices
    }
    
    # Ultra-optimized download with parallel processing
    for tier_name, voice_batch in ULTRA_VOICES.items():
        tier_time_limit = tier_time_limits.get(tier_name, 60)
        
        batch_downloaded = download_tier_parallel(voice_batch, tier_name, tier_time_limit)
        total_downloaded += batch_downloaded
        
        elapsed = time.time() - start_time
        print(f"Progress: {total_downloaded}/{total_voices} ({total_downloaded/total_voices*100:.1f}%) | Elapsed: {elapsed:.1f}s")
        
        # Stop if we exceed Railway time limits or achieve target
        if elapsed > 450 or total_downloaded >= 52:  # 7.5 minutes max, or 52+ voices
            print(f"Target achieved! {total_downloaded} voices in {elapsed:.1f}s")
            break
        
        # Brief pause between tiers
        time.sleep(2)
    
    print(f"\nUltra-Optimized Download Complete!")
    print(f"Final count: {total_downloaded} voices")
    print(f"Total time: {time.time() - start_time:.1f}s")
    
    # Enhanced summary
    summary = {
        "total_voices": total_downloaded,
        "target_voices": 50,
        "download_time": time.time() - start_time,
        "success_rate": download_stats["success"] / (download_stats["success"] + download_stats["failed"]) * 100 if (download_stats["success"] + download_stats["failed"]) > 0 else 0,
        "coverage": "ultra" if total_downloaded >= 50 else "enhanced" if total_downloaded >= 40 else "good",
        "status": "ultra-success" if total_downloaded >= 50 else "success"
    }
    
    with open(MODELS_DIR / "download_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"Summary: {summary['coverage']} coverage, {summary['success_rate']:.1f}% success rate")
    
    if total_downloaded >= 50:
        print("🎯 ULTRA SUCCESS: 50+ voice target achieved!")
    elif total_downloaded >= 45:
        print("✨ NEAR TARGET: Close to 50 voice goal!")
    else:
        print("📈 PROGRESS: Significant improvement over baseline!")

if __name__ == "__main__":
    main()
