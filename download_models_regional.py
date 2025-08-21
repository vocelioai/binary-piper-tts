#!/usr/bin/env python3
"""
Regional Voice Deployment - Target specific markets
Configure for specific geographic regions or business needs
"""
import os
import urllib.request
import urllib.error
from pathlib import Path
import json
import time

MODELS_DIR = Path("models")
MODELS_DIR.mkdir(exist_ok=True)

BASE_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/main"

# Regional voice configurations
REGIONAL_CONFIGS = {
    "north_america": {
        "description": "North American English variants",
        "voices": {
            "en_US-lessac-medium": [f"{BASE_URL}/en/en_US/lessac/medium/en_US-lessac-medium.onnx", f"{BASE_URL}/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json"],
            "en_US-amy-low": [f"{BASE_URL}/en/en_US/amy/low/en_US-amy-low.onnx", f"{BASE_URL}/en/en_US/amy/low/en_US-amy-low.onnx.json"],
            "en_US-danny-low": [f"{BASE_URL}/en/en_US/danny/low/en_US-danny-low.onnx", f"{BASE_URL}/en/en_US/danny/low/en_US-danny-low.onnx.json"],
            "en_US-kathleen-low": [f"{BASE_URL}/en/en_US/kathleen/low/en_US-kathleen-low.onnx", f"{BASE_URL}/en/en_US/kathleen/low/en_US-kathleen-low.onnx.json"],
            "en_US-ryan-medium": [f"{BASE_URL}/en/en_US/ryan/medium/en_US-ryan-medium.onnx", f"{BASE_URL}/en/en_US/ryan/medium/en_US-ryan-medium.onnx.json"],
            "en_US-ljspeech-medium": [f"{BASE_URL}/en/en_US/ljspeech/medium/en_US-ljspeech-medium.onnx", f"{BASE_URL}/en/en_US/ljspeech/medium/en_US-ljspeech-medium.onnx.json"]
        }
    },
    
    "europe": {
        "description": "Major European languages",
        "voices": {
            "en_GB-cori-medium": [f"{BASE_URL}/en/en_GB/cori/medium/en_GB-cori-medium.onnx", f"{BASE_URL}/en/en_GB/cori/medium/en_GB-cori-medium.onnx.json"],
            "de_DE-thorsten-medium": [f"{BASE_URL}/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx", f"{BASE_URL}/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx.json"],
            "fr_FR-siwis-medium": [f"{BASE_URL}/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx", f"{BASE_URL}/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx.json"],
            "es_ES-davefx-medium": [f"{BASE_URL}/es/es_ES/davefx/medium/es_ES-davefx-medium.onnx", f"{BASE_URL}/es/es_ES/davefx/medium/es_ES-davefx-medium.onnx.json"],
            "it_IT-riccardo-x_low": [f"{BASE_URL}/it/it_IT/riccardo/x_low/it_IT-riccardo-x_low.onnx", f"{BASE_URL}/it/it_IT/riccardo/x_low/it_IT-riccardo-x_low.onnx.json"],
            "pt_BR-faber-medium": [f"{BASE_URL}/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx", f"{BASE_URL}/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx.json"],
            "nl_NL-mls_5809-low": [f"{BASE_URL}/nl/nl_NL/mls_5809/low/nl_NL-mls_5809-low.onnx", f"{BASE_URL}/nl/nl_NL/mls_5809/low/nl_NL-mls_5809-low.onnx.json"],
            "sv_SE-nst-medium": [f"{BASE_URL}/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx", f"{BASE_URL}/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx.json"],
            "da_DK-talesyntese-medium": [f"{BASE_URL}/da/da_DK/talesyntese/medium/da_DK-talesyntese-medium.onnx", f"{BASE_URL}/da/da_DK/talesyntese/medium/da_DK-talesyntese-medium.onnx.json"],
            "no_NO-talesyntese-medium": [f"{BASE_URL}/no/no_NO/talesyntese/medium/no_NO-talesyntese-medium.onnx", f"{BASE_URL}/no/no_NO/talesyntese/medium/no_NO-talesyntese-medium.onnx.json"]
        }
    },
    
    "asia_pacific": {
        "description": "Asia-Pacific major languages",
        "voices": {
            "zh_CN-huayan-medium": [f"{BASE_URL}/zh/zh_CN/huayan/medium/zh_CN-huayan-medium.onnx", f"{BASE_URL}/zh/zh_CN/huayan/medium/zh_CN-huayan-medium.onnx.json"],
            "ja_JP-kaiueo-medium": [f"{BASE_URL}/ja/ja_JP/kaiueo/medium/ja_JP-kaiueo-medium.onnx", f"{BASE_URL}/ja/ja_JP/kaiueo/medium/ja_JP-kaiueo-medium.onnx.json"],
            "vi_VN-vivos-x_low": [f"{BASE_URL}/vi/vi_VN/vivos/x_low/vi_VN-vivos-x_low.onnx", f"{BASE_URL}/vi/vi_VN/vivos/x_low/vi_VN-vivos-x_low.onnx.json"],
            "en_US-lessac-medium": [f"{BASE_URL}/en/en_US/lessac/medium/en_US-lessac-medium.onnx", f"{BASE_URL}/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json"],
            "en_GB-cori-medium": [f"{BASE_URL}/en/en_GB/cori/medium/en_GB-cori-medium.onnx", f"{BASE_URL}/en/en_GB/cori/medium/en_GB-cori-medium.onnx.json"]
        }
    },
    
    "global_business": {
        "description": "Top business languages worldwide",
        "voices": {
            "en_US-lessac-medium": [f"{BASE_URL}/en/en_US/lessac/medium/en_US-lessac-medium.onnx", f"{BASE_URL}/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json"],
            "en_GB-cori-medium": [f"{BASE_URL}/en/en_GB/cori/medium/en_GB-cori-medium.onnx", f"{BASE_URL}/en/en_GB/cori/medium/en_GB-cori-medium.onnx.json"],
            "zh_CN-huayan-medium": [f"{BASE_URL}/zh/zh_CN/huayan/medium/zh_CN-huayan-medium.onnx", f"{BASE_URL}/zh/zh_CN/huayan/medium/zh_CN-huayan-medium.onnx.json"],
            "es_ES-davefx-medium": [f"{BASE_URL}/es/es_ES/davefx/medium/es_ES-davefx-medium.onnx", f"{BASE_URL}/es/es_ES/davefx/medium/es_ES-davefx-medium.onnx.json"],
            "fr_FR-siwis-medium": [f"{BASE_URL}/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx", f"{BASE_URL}/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx.json"],
            "de_DE-thorsten-medium": [f"{BASE_URL}/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx", f"{BASE_URL}/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx.json"],
            "ja_JP-kaiueo-medium": [f"{BASE_URL}/ja/ja_JP/kaiueo/medium/ja_JP-kaiueo-medium.onnx", f"{BASE_URL}/ja/ja_JP/kaiueo/medium/ja_JP-kaiueo-medium.onnx.json"],
            "ar_JO-kareem-medium": [f"{BASE_URL}/ar/ar_JO/kareem/medium/ar_JO-kareem-medium.onnx", f"{BASE_URL}/ar/ar_JO/kareem/medium/ar_JO-kareem-medium.onnx.json"],
            "ru_RU-dmitri-medium": [f"{BASE_URL}/ru/ru_RU/dmitri/medium/ru_RU-dmitri-medium.onnx", f"{BASE_URL}/ru/ru_RU/dmitri/medium/ru_RU-dmitri-medium.onnx.json"],
            "pt_BR-faber-medium": [f"{BASE_URL}/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx", f"{BASE_URL}/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx.json"]
        }
    }
}

def download_file(url, filepath, max_retries=3):
    """Download a file with error handling"""
    for attempt in range(max_retries):
        try:
            print(f"  📥 {filepath.name}...")
            urllib.request.urlretrieve(url, filepath)
            return True
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"  ⚠️ Retry {attempt + 1}/{max_retries}")
                time.sleep(2)
            else:
                print(f"  ❌ Failed: {str(e)[:50]}")
                return False
    return False

def main():
    """Regional voice deployment"""
    # Auto-detect region preference or use environment variable
    region = os.environ.get("VOICE_REGION", "global_business").lower()
    
    if region not in REGIONAL_CONFIGS:
        print(f"⚠️ Unknown region '{region}', using 'global_business'")
        region = "global_business"
    
    config = REGIONAL_CONFIGS[region]
    print(f"🚀 Binary Piper TTS - Regional Deployment: {region.replace('_', ' ').title()}")
    print(f"📋 {config['description']}")
    print(f"🎯 Downloading {len(config['voices'])} voices...\n")
    
    start_time = time.time()
    downloaded = 0
    total = len(config['voices'])
    
    for voice_id, urls in config['voices'].items():
        print(f"📦 {voice_id}...")
        
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
        print()
    
    # Summary
    elapsed = time.time() - start_time
    print(f"🎉 Regional Deployment Complete!")
    print(f"📊 Downloaded: {downloaded}/{total} voices")
    print(f"⏱️ Time: {elapsed:.1f}s")
    print(f"🌍 Region: {region.replace('_', ' ').title()}")
    
    # Create summary
    summary = {
        "deployment_type": "regional",
        "region": region,
        "total_voices": downloaded,
        "success_rate": f"{downloaded}/{total}",
        "download_time": elapsed
    }
    
    with open(MODELS_DIR / "regional_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

if __name__ == "__main__":
    main()
