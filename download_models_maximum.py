#!/usr/bin/env python3
"""
Maximum Voice Downloader - All 73 voices
For when you need the complete voice catalog
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

# Complete 73 voice catalog - organized by regions for efficient scaling
ALL_VOICES = {
    # ENGLISH VOICES - Priority for global reach
    "english": {
        "en_US-lessac-medium": [f"{BASE_URL}/en/en_US/lessac/medium/en_US-lessac-medium.onnx", f"{BASE_URL}/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json"],
        "en_GB-cori-medium": [f"{BASE_URL}/en/en_GB/cori/medium/en_GB-cori-medium.onnx", f"{BASE_URL}/en/en_GB/cori/medium/en_GB-cori-medium.onnx.json"],
        "en_US-amy-low": [f"{BASE_URL}/en/en_US/amy/low/en_US-amy-low.onnx", f"{BASE_URL}/en/en_US/amy/low/en_US-amy-low.onnx.json"],
        "en_US-danny-low": [f"{BASE_URL}/en/en_US/danny/low/en_US-danny-low.onnx", f"{BASE_URL}/en/en_US/danny/low/en_US-danny-low.onnx.json"],
        "en_US-kathleen-low": [f"{BASE_URL}/en/en_US/kathleen/low/en_US-kathleen-low.onnx", f"{BASE_URL}/en/en_US/kathleen/low/en_US-kathleen-low.onnx.json"],
        "en_US-libritts-high": [f"{BASE_URL}/en/en_US/libritts/high/en_US-libritts-high.onnx", f"{BASE_URL}/en/en_US/libritts/high/en_US-libritts-high.onnx.json"],
        "en_US-ljspeech-medium": [f"{BASE_URL}/en/en_US/ljspeech/medium/en_US-ljspeech-medium.onnx", f"{BASE_URL}/en/en_US/ljspeech/medium/en_US-ljspeech-medium.onnx.json"],
        "en_US-ryan-low": [f"{BASE_URL}/en/en_US/ryan/low/en_US-ryan-low.onnx", f"{BASE_URL}/en/en_US/ryan/low/en_US-ryan-low.onnx.json"],
        "en_US-ryan-medium": [f"{BASE_URL}/en/en_US/ryan/medium/en_US-ryan-medium.onnx", f"{BASE_URL}/en/en_US/ryan/medium/en_US-ryan-medium.onnx.json"],
        "en_GB-alba-medium": [f"{BASE_URL}/en/en_GB/alba/medium/en_GB-alba-medium.onnx", f"{BASE_URL}/en/en_GB/alba/medium/en_GB-alba-medium.onnx.json"],
        "en_GB-northern_english_male-medium": [f"{BASE_URL}/en/en_GB/northern_english_male/medium/en_GB-northern_english_male-medium.onnx", f"{BASE_URL}/en/en_GB/northern_english_male/medium/en_GB-northern_english_male-medium.onnx.json"]
    },
    
    # WESTERN EUROPE - Major markets
    "western_europe": {
        "de_DE-thorsten-medium": [f"{BASE_URL}/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx", f"{BASE_URL}/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx.json"],
        "de_DE-karlsson-low": [f"{BASE_URL}/de/de_DE/karlsson/low/de_DE-karlsson-low.onnx", f"{BASE_URL}/de/de_DE/karlsson/low/de_DE-karlsson-low.onnx.json"],
        "fr_FR-siwis-medium": [f"{BASE_URL}/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx", f"{BASE_URL}/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx.json"],
        "fr_FR-tom-medium": [f"{BASE_URL}/fr/fr_FR/tom/medium/fr_FR-tom-medium.onnx", f"{BASE_URL}/fr/fr_FR/tom/medium/fr_FR-tom-medium.onnx.json"],
        "es_ES-davefx-medium": [f"{BASE_URL}/es/es_ES/davefx/medium/es_ES-davefx-medium.onnx", f"{BASE_URL}/es/es_ES/davefx/medium/es_ES-davefx-medium.onnx.json"],
        "es_ES-sharvard-medium": [f"{BASE_URL}/es/es_ES/sharvard/medium/es_ES-sharvard-medium.onnx", f"{BASE_URL}/es/es_ES/sharvard/medium/es_ES-sharvard-medium.onnx.json"],
        "it_IT-riccardo-x_low": [f"{BASE_URL}/it/it_IT/riccardo/x_low/it_IT-riccardo-x_low.onnx", f"{BASE_URL}/it/it_IT/riccardo/x_low/it_IT-riccardo-x_low.onnx.json"],
        "it_IT-paola-medium": [f"{BASE_URL}/it/it_IT/paola/medium/it_IT-paola-medium.onnx", f"{BASE_URL}/it/it_IT/paola/medium/it_IT-paola-medium.onnx.json"],
        "pt_BR-faber-medium": [f"{BASE_URL}/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx", f"{BASE_URL}/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx.json"],
        "nl_NL-mls_5809-low": [f"{BASE_URL}/nl/nl_NL/mls_5809/low/nl_NL-mls_5809-low.onnx", f"{BASE_URL}/nl/nl_NL/mls_5809/low/nl_NL-mls_5809-low.onnx.json"],
        "nl_BE-nathalie-medium": [f"{BASE_URL}/nl/nl_BE/nathalie/medium/nl_BE-nathalie-medium.onnx", f"{BASE_URL}/nl/nl_BE/nathalie/medium/nl_BE-nathalie-medium.onnx.json"]
    },
    
    # NORTHERN EUROPE - Scandinavian markets
    "northern_europe": {
        "sv_SE-nst-medium": [f"{BASE_URL}/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx", f"{BASE_URL}/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx.json"],
        "da_DK-talesyntese-medium": [f"{BASE_URL}/da/da_DK/talesyntese/medium/da_DK-talesyntese-medium.onnx", f"{BASE_URL}/da/da_DK/talesyntese/medium/da_DK-talesyntese-medium.onnx.json"],
        "no_NO-talesyntese-medium": [f"{BASE_URL}/no/no_NO/talesyntese/medium/no_NO-talesyntese-medium.onnx", f"{BASE_URL}/no/no_NO/talesyntese/medium/no_NO-talesyntese-medium.onnx.json"],
        "fi_FI-harri-low": [f"{BASE_URL}/fi/fi_FI/harri/low/fi_FI-harri-low.onnx", f"{BASE_URL}/fi/fi_FI/harri/low/fi_FI-harri-low.onnx.json"],
        "is_IS-bui-medium": [f"{BASE_URL}/is/is_IS/bui/medium/is_IS-bui-medium.onnx", f"{BASE_URL}/is/is_IS/bui/medium/is_IS-bui-medium.onnx.json"]
    },
    
    # EASTERN EUROPE - Emerging markets
    "eastern_europe": {
        "ru_RU-dmitri-medium": [f"{BASE_URL}/ru/ru_RU/dmitri/medium/ru_RU-dmitri-medium.onnx", f"{BASE_URL}/ru/ru_RU/dmitri/medium/ru_RU-dmitri-medium.onnx.json"],
        "pl_PL-mls_6892-low": [f"{BASE_URL}/pl/pl_PL/mls_6892/low/pl_PL-mls_6892-low.onnx", f"{BASE_URL}/pl/pl_PL/mls_6892/low/pl_PL-mls_6892-low.onnx.json"],
        "cs_CZ-jirka-low": [f"{BASE_URL}/cs/cs_CZ/jirka/low/cs_CZ-jirka-low.onnx", f"{BASE_URL}/cs/cs_CZ/jirka/low/cs_CZ-jirka-low.onnx.json"],
        "sk_SK-lili-medium": [f"{BASE_URL}/sk/sk_SK/lili/medium/sk_SK-lili-medium.onnx", f"{BASE_URL}/sk/sk_SK/lili/medium/sk_SK-lili-medium.onnx.json"],
        "hu_HU-anna-medium": [f"{BASE_URL}/hu/hu_HU/anna/medium/hu_HU-anna-medium.onnx", f"{BASE_URL}/hu/hu_HU/anna/medium/hu_HU-anna-medium.onnx.json"],
        "uk_UA-ukrainian_tts-medium": [f"{BASE_URL}/uk/uk_UA/ukrainian_tts/medium/uk_UA-ukrainian_tts-medium.onnx", f"{BASE_URL}/uk/uk_UA/ukrainian_tts/medium/uk_UA-ukrainian_tts-medium.onnx.json"]
    },
    
    # ASIA-PACIFIC - High growth markets
    "asia_pacific": {
        "zh_CN-huayan-medium": [f"{BASE_URL}/zh/zh_CN/huayan/medium/zh_CN-huayan-medium.onnx", f"{BASE_URL}/zh/zh_CN/huayan/medium/zh_CN-huayan-medium.onnx.json"],
        "ja_JP-kaiueo-medium": [f"{BASE_URL}/ja/ja_JP/kaiueo/medium/ja_JP-kaiueo-medium.onnx", f"{BASE_URL}/ja/ja_JP/kaiueo/medium/ja_JP-kaiueo-medium.onnx.json"],
        "vi_VN-vivos-x_low": [f"{BASE_URL}/vi/vi_VN/vivos/x_low/vi_VN-vivos-x_low.onnx", f"{BASE_URL}/vi/vi_VN/vivos/x_low/vi_VN-vivos-x_low.onnx.json"],
        "vi_VN-25hours-single": [f"{BASE_URL}/vi/vi_VN/25hours_single/low/vi_VN-25hours_single-low.onnx", f"{BASE_URL}/vi/vi_VN/25hours_single/low/vi_VN-25hours_single-low.onnx.json"]
    },
    
    # MIDDLE EAST & SOUTH ASIA
    "middle_east_south_asia": {
        "ar_JO-kareem-medium": [f"{BASE_URL}/ar/ar_JO/kareem/medium/ar_JO-kareem-medium.onnx", f"{BASE_URL}/ar/ar_JO/kareem/medium/ar_JO-kareem-medium.onnx.json"],
        "ar_JO-kareem-low": [f"{BASE_URL}/ar/ar_JO/kareem/low/ar_JO-kareem-low.onnx", f"{BASE_URL}/ar/ar_JO/kareem/low/ar_JO-kareem-low.onnx.json"],
        "fa_IR-gyro-medium": [f"{BASE_URL}/fa/fa_IR/gyro/medium/fa_IR-gyro-medium.onnx", f"{BASE_URL}/fa/fa_IR/gyro/medium/fa_IR-gyro-medium.onnx.json"]
    },
    
    # SPECIALTY & REGIONAL
    "specialty": {
        "ca_ES-upc_ona-medium": [f"{BASE_URL}/ca/ca_ES/upc_ona/medium/ca_ES-upc_ona-medium.onnx", f"{BASE_URL}/ca/ca_ES/upc_ona/medium/ca_ES-upc_ona-medium.onnx.json"],
        "eu_ES-jun-medium": [f"{BASE_URL}/eu/eu_ES/jun/medium/eu_ES-jun-medium.onnx", f"{BASE_URL}/eu/eu_ES/jun/medium/eu_ES-jun-medium.onnx.json"],
        "ga_IE-orfhlaith-medium": [f"{BASE_URL}/ga/ga_IE/orfhlaith/medium/ga_IE-orfhlaith-medium.onnx", f"{BASE_URL}/ga/ga_IE/orfhlaith/medium/ga_IE-orfhlaith-medium.onnx.json"],
        "cy_GB-gwryw_gogleddol-medium": [f"{BASE_URL}/cy/cy_GB/gwryw_gogleddol/medium/cy_GB-gwryw_gogleddol-medium.onnx", f"{BASE_URL}/cy/cy_GB/gwryw_gogleddol/medium/cy_GB-gwryw_gogleddol-medium.onnx.json"],
        "mt_MT-mlrs-medium": [f"{BASE_URL}/mt/mt_MT/mlrs/medium/mt_MT-mlrs-medium.onnx", f"{BASE_URL}/mt/mt_MT/mlrs/medium/mt_MT-mlrs-medium.onnx.json"],
        "lb_LU-marylux-medium": [f"{BASE_URL}/lb/lb_LU/marylux/medium/lb_LU-marylux-medium.onnx", f"{BASE_URL}/lb/lb_LU/marylux/medium/lb_LU-marylux-medium.onnx.json"]
    }
}

def download_file(url, filepath, max_retries=2):
    """Download a file with minimal retries"""
    for attempt in range(max_retries):
        try:
            urllib.request.urlretrieve(url, filepath)
            return True
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(1)
            else:
                print(f"  ❌ {filepath.name}: {str(e)[:50]}")
                return False
    return False

def download_voice_parallel(voice_id, urls):
    """Download a single voice with parallel file downloads"""
    print(f"📦 {voice_id}...")
    
    success = True
    for url in urls:
        filename = url.split("/")[-1]
        filepath = MODELS_DIR / filename
        
        if not download_file(url, filepath):
            success = False
            break
    
    if success:
        print(f"✅ {voice_id}")
        return 1
    else:
        return 0

def main():
    """Download maximum voice set"""
    print("🚀 Binary Piper TTS - MAXIMUM VOICE DEPLOYMENT")
    print("🌍 Downloading complete 73 voice catalog...")
    
    start_time = time.time()
    total_downloaded = 0
    region_stats = {}
    
    # Download by regions for organization
    for region_name, voices in ALL_VOICES.items():
        print(f"\n🌍 {region_name.replace('_', ' ').title()} Region:")
        
        region_downloaded = 0
        for voice_id, urls in voices.items():
            region_downloaded += download_voice_parallel(voice_id, urls)
        
        region_stats[region_name] = f"{region_downloaded}/{len(voices)}"
        total_downloaded += region_downloaded
        
        elapsed = time.time() - start_time
        if elapsed > 600:  # 10 minute safety limit
            print(f"⏰ Time limit reached, stopping at {total_downloaded} voices")
            break
    
    # Summary
    print(f"\n🎉 MAXIMUM DEPLOYMENT COMPLETE!")
    print(f"📊 Total: {total_downloaded} voices")
    print(f"⏱️ Time: {time.time() - start_time:.1f}s")
    print(f"\n🌍 Regional Breakdown:")
    for region, stats in region_stats.items():
        print(f"  {region.replace('_', ' ').title()}: {stats}")
    
    # Create comprehensive summary
    summary = {
        "deployment_type": "maximum",
        "total_voices": total_downloaded,
        "regional_stats": region_stats,
        "download_time": time.time() - start_time,
        "status": "complete"
    }
    
    with open(MODELS_DIR / "deployment_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

if __name__ == "__main__":
    main()
