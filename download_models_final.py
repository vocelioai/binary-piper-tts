#!/usr/bin/env python3
"""
Final Optimized voice downloader - Using proven URLs from enhanced downloader
Sequential download targeting 50+ voices with maximum reliability
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

# Proven voice URLs from enhanced downloader - optimized order for 50+ voices
PROVEN_VOICES = [
    # Tier 1: Small/fast files first (16 voices)
    ("en_US-amy-low", [f"{BASE_URL}/en/en_US/amy/low/en_US-amy-low.onnx", f"{BASE_URL}/en/en_US/amy/low/en_US-amy-low.onnx.json"]),
    ("en_US-danny-low", [f"{BASE_URL}/en/en_US/danny/low/en_US-danny-low.onnx", f"{BASE_URL}/en/en_US/danny/low/en_US-danny-low.onnx.json"]),
    ("en_US-kathleen-low", [f"{BASE_URL}/en/en_US/kathleen/low/en_US-kathleen-low.onnx", f"{BASE_URL}/en/en_US/kathleen/low/en_US-kathleen-low.onnx.json"]),
    ("it_IT-riccardo-x_low", [f"{BASE_URL}/it/it_IT/riccardo/x_low/it_IT-riccardo-x_low.onnx", f"{BASE_URL}/it/it_IT/riccardo/x_low/it_IT-riccardo-x_low.onnx.json"]),
    ("fr_FR-mls_1840-low", [f"{BASE_URL}/fr/fr_FR/mls_1840/low/fr_FR-mls_1840-low.onnx", f"{BASE_URL}/fr/fr_FR/mls_1840/low/fr_FR-mls_1840-low.onnx.json"]),
    ("de_DE-mls_9972-low", [f"{BASE_URL}/de/de_DE/mls_9972/low/de_DE-mls_9972-low.onnx", f"{BASE_URL}/de/de_DE/mls_9972/low/de_DE-mls_9972-low.onnx.json"]),
    ("nl_NL-mls_5809-low", [f"{BASE_URL}/nl/nl_NL/mls_5809/low/nl_NL-mls_5809-low.onnx", f"{BASE_URL}/nl/nl_NL/mls_5809/low/nl_NL-mls_5809-low.onnx.json"]),
    ("pl_PL-mls_6892-low", [f"{BASE_URL}/pl/pl_PL/mls_6892/low/pl_PL-mls_6892-low.onnx", f"{BASE_URL}/pl/pl_PL/mls_6892/low/pl_PL-mls_6892-low.onnx.json"]),
    ("cs_CZ-jirka-low", [f"{BASE_URL}/cs/cs_CZ/jirka/low/cs_CZ-jirka-low.onnx", f"{BASE_URL}/cs/cs_CZ/jirka/low/cs_CZ-jirka-low.onnx.json"]),
    ("fi_FI-harri-low", [f"{BASE_URL}/fi/fi_FI/harri/low/fi_FI-harri-low.onnx", f"{BASE_URL}/fi/fi_FI/harri/low/fi_FI-harri-low.onnx.json"]),
    ("vi_VN-vivos-x_low", [f"{BASE_URL}/vi/vi_VN/vivos/x_low/vi_VN-vivos-x_low.onnx", f"{BASE_URL}/vi/vi_VN/vivos/x_low/vi_VN-vivos-x_low.onnx.json"]),
    ("fr_FR-tom-x_low", [f"{BASE_URL}/fr/fr_FR/tom/x_low/fr_FR-tom-x_low.onnx", f"{BASE_URL}/fr/fr_FR/tom/x_low/fr_FR-tom-x_low.onnx.json"]),
    ("de_DE-eva_k-x_low", [f"{BASE_URL}/de/de_DE/eva_k/x_low/de_DE-eva_k-x_low.onnx", f"{BASE_URL}/de/de_DE/eva_k/x_low/de_DE-eva_k-x_low.onnx.json"]),
    ("el_GR-rapunzelina-low", [f"{BASE_URL}/el/el_GR/rapunzelina/low/el_GR-rapunzelina-low.onnx", f"{BASE_URL}/el/el_GR/rapunzelina/low/el_GR-rapunzelina-low.onnx.json"]),
    ("fr_CA-pol-low", [f"{BASE_URL}/fr/fr_CA/pol/low/fr_CA-pol-low.onnx", f"{BASE_URL}/fr/fr_CA/pol/low/fr_CA-pol-low.onnx.json"]),
    
    # Tier 2: Essential medium quality (20 voices)
    ("en_US-lessac-medium", [f"{BASE_URL}/en/en_US/lessac/medium/en_US-lessac-medium.onnx", f"{BASE_URL}/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json"]),
    ("en_GB-cori-medium", [f"{BASE_URL}/en/en_GB/cori/medium/en_GB-cori-medium.onnx", f"{BASE_URL}/en/en_GB/cori/medium/en_GB-cori-medium.onnx.json"]),
    ("en_GB-alba-medium", [f"{BASE_URL}/en/en_GB/alba/medium/en_GB-alba-medium.onnx", f"{BASE_URL}/en/en_GB/alba/medium/en_GB-alba-medium.onnx.json"]),
    ("es_ES-davefx-medium", [f"{BASE_URL}/es/es_ES/davefx/medium/es_ES-davefx-medium.onnx", f"{BASE_URL}/es/es_ES/davefx/medium/es_ES-davefx-medium.onnx.json"]),
    ("es_ES-sharvard-medium", [f"{BASE_URL}/es/es_ES/sharvard/medium/es_ES-sharvard-medium.onnx", f"{BASE_URL}/es/es_ES/sharvard/medium/es_ES-sharvard-medium.onnx.json"]),
    ("fr_FR-siwis-medium", [f"{BASE_URL}/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx", f"{BASE_URL}/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx.json"]),
    ("de_DE-thorsten-medium", [f"{BASE_URL}/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx", f"{BASE_URL}/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx.json"]),
    ("it_IT-paola-medium", [f"{BASE_URL}/it/it_IT/paola/medium/it_IT-paola-medium.onnx", f"{BASE_URL}/it/it_IT/paola/medium/it_IT-paola-medium.onnx.json"]),
    ("pt_BR-faber-medium", [f"{BASE_URL}/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx", f"{BASE_URL}/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx.json"]),
    ("ru_RU-dmitri-medium", [f"{BASE_URL}/ru/ru_RU/dmitri/medium/ru_RU-dmitri-medium.onnx", f"{BASE_URL}/ru/ru_RU/dmitri/medium/ru_RU-dmitri-medium.onnx.json"]),
    ("nl_NL-rdh-medium", [f"{BASE_URL}/nl/nl_NL/rdh/medium/nl_NL-rdh-medium.onnx", f"{BASE_URL}/nl/nl_NL/rdh/medium/nl_NL-rdh-medium.onnx.json"]),
    ("sv_SE-nst-medium", [f"{BASE_URL}/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx", f"{BASE_URL}/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx.json"]),
    ("da_DK-talesyntese-medium", [f"{BASE_URL}/da/da_DK/talesyntese/medium/da_DK-talesyntese-medium.onnx", f"{BASE_URL}/da/da_DK/talesyntese/medium/da_DK-talesyntese-medium.onnx.json"]),
    ("no_NO-talesyntese-medium", [f"{BASE_URL}/no/no_NO/talesyntese/medium/no_NO-talesyntese-medium.onnx", f"{BASE_URL}/no/no_NO/talesyntese/medium/no_NO-talesyntese-medium.onnx.json"]),
    ("zh_CN-huayan-medium", [f"{BASE_URL}/zh/zh_CN/huayan/medium/zh_CN-huayan-medium.onnx", f"{BASE_URL}/zh/zh_CN/huayan/medium/zh_CN-huayan-medium.onnx.json"]),
    ("ja_JP-kaiueo-medium", [f"{BASE_URL}/ja/ja_JP/kaiueo/medium/ja_JP-kaiueo-medium.onnx", f"{BASE_URL}/ja/ja_JP/kaiueo/medium/ja_JP-kaiueo-medium.onnx.json"]),
    ("ca_ES-upc_ona-medium", [f"{BASE_URL}/ca/ca_ES/upc_ona/medium/ca_ES-upc_ona-medium.onnx", f"{BASE_URL}/ca/ca_ES/upc_ona/medium/ca_ES-upc_ona-medium.onnx.json"]),
    ("hu_HU-anna-medium", [f"{BASE_URL}/hu/hu_HU/anna/medium/hu_HU-anna-medium.onnx", f"{BASE_URL}/hu/hu_HU/anna/medium/hu_HU-anna-medium.onnx.json"]),
    ("tr_TR-dfki-medium", [f"{BASE_URL}/tr/tr_TR/dfki/medium/tr_TR-dfki-medium.onnx", f"{BASE_URL}/tr/tr_TR/dfki/medium/tr_TR-dfki-medium.onnx.json"]),
    ("uk_UA-ukrainian_tts-medium", [f"{BASE_URL}/uk/uk_UA/ukrainian_tts/medium/uk_UA-ukrainian_tts-medium.onnx", f"{BASE_URL}/uk/uk_UA/ukrainian_tts/medium/uk_UA-ukrainian_tts-medium.onnx.json"]),
    ("ro_RO-mihai-medium", [f"{BASE_URL}/ro/ro_RO/mihai/medium/ro_RO-mihai-medium.onnx", f"{BASE_URL}/ro/ro_RO/mihai/medium/ro_RO-mihai-medium.onnx.json"]),
    ("bg_BG-krastyo-medium", [f"{BASE_URL}/bg/bg_BG/krastyo/medium/bg_BG-krastyo-medium.onnx", f"{BASE_URL}/bg/bg_BG/krastyo/medium/bg_BG-krastyo-medium.onnx.json"]),
    ("ar_JO-kareem-medium", [f"{BASE_URL}/ar/ar_JO/kareem/medium/ar_JO-kareem-medium.onnx", f"{BASE_URL}/ar/ar_JO/kareem/medium/ar_JO-kareem-medium.onnx.json"]),
    ("hi_IN-male-medium", [f"{BASE_URL}/hi/hi_IN/male/medium/hi_IN-male-medium.onnx", f"{BASE_URL}/hi/hi_IN/male/medium/hi_IN-male-medium.onnx.json"]),
    ("ko_KR-kss-medium", [f"{BASE_URL}/ko/ko_KR/kss/medium/ko_KR-kss-medium.onnx", f"{BASE_URL}/ko/ko_KR/kss/medium/ko_KR-kss-medium.onnx.json"]),
    ("th_TH-kaiueo-medium", [f"{BASE_URL}/th/th_TH/kaiueo/medium/th_TH-kaiueo-medium.onnx", f"{BASE_URL}/th/th_TH/kaiueo/medium/th_TH-kaiueo-medium.onnx.json"]),
    ("fa_IR-gyro-medium", [f"{BASE_URL}/fa/fa_IR/gyro/medium/fa_IR-gyro-medium.onnx", f"{BASE_URL}/fa/fa_IR/gyro/medium/fa_IR-gyro-medium.onnx.json"]),
    ("he_IL-amitai-medium", [f"{BASE_URL}/he/he_IL/amitai/medium/he_IL-amitai-medium.onnx", f"{BASE_URL}/he/he_IL/amitai/medium/he_IL-amitai-medium.onnx.json"]),
    
    # Tier 3: Additional variants (16+ voices for 50+ total)
    ("en_US-joe-medium", [f"{BASE_URL}/en/en_US/joe/medium/en_US-joe-medium.onnx", f"{BASE_URL}/en/en_US/joe/medium/en_US-joe-medium.onnx.json"]),
    ("en_GB-jenny_dioco-medium", [f"{BASE_URL}/en/en_GB/jenny_dioco/medium/en_GB-jenny_dioco-medium.onnx", f"{BASE_URL}/en/en_GB/jenny_dioco/medium/en_GB-jenny_dioco-medium.onnx.json"]),
    ("es_MX-ald-medium", [f"{BASE_URL}/es/es_MX/ald/medium/es_MX-ald-medium.onnx", f"{BASE_URL}/es/es_MX/ald/medium/es_MX-ald-medium.onnx.json"]),
    ("pt_PT-tugao-medium", [f"{BASE_URL}/pt/pt_PT/tugao/medium/pt_PT-tugao-medium.onnx", f"{BASE_URL}/pt/pt_PT/tugao/medium/pt_PT-tugao-medium.onnx.json"]),
    ("de_AT-hagen-medium", [f"{BASE_URL}/de/de_AT/hagen/medium/de_AT-hagen-medium.onnx", f"{BASE_URL}/de/de_AT/hagen/medium/de_AT-hagen-medium.onnx.json"]),
    ("zh_TW-fgl-medium", [f"{BASE_URL}/zh/zh_TW/fgl/medium/zh_TW-fgl-medium.onnx", f"{BASE_URL}/zh/zh_TW/fgl/medium/zh_TW-fgl-medium.onnx.json"]),
    ("sl_SI-artur-medium", [f"{BASE_URL}/sl/sl_SI/artur/medium/sl_SI-artur-medium.onnx", f"{BASE_URL}/sl/sl_SI/artur/medium/sl_SI-artur-medium.onnx.json"]),
    ("sk_SK-lili-medium", [f"{BASE_URL}/sk/sk_SK/lili/medium/sk_SK-lili-medium.onnx", f"{BASE_URL}/sk/sk_SK/lili/medium/sk_SK-lili-medium.onnx.json"]),
    ("en_US-ryan-high", [f"{BASE_URL}/en/en_US/ryan/high/en_US-ryan-high.onnx", f"{BASE_URL}/en/en_US/ryan/high/en_US-ryan-high.onnx.json"]),
]

def download_file_optimized(url, filepath, timeout=45):
    """Download with optimized settings"""
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        
        with urllib.request.urlopen(req, timeout=timeout) as response:
            with open(filepath, 'wb') as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f"    Failed: {e}")
        return False

def download_voice_optimized(voice_id, urls):
    """Download a voice with optimized approach"""
    print(f"  {voice_id}...")
    
    for url in urls:
        filename = url.split("/")[-1]
        filepath = MODELS_DIR / filename
        
        if not download_file_optimized(url, filepath):
            return False
            
    return True

def main():
    """Final optimized download targeting 50+ voices"""
    print("Binary Piper TTS - Final Optimized Download")
    print("Target: 50+ voices with proven URLs and maximum efficiency")
    
    total_downloaded = 0
    start_time = time.time()
    
    print(f"Total voices available: {len(PROVEN_VOICES)}")
    
    for i, (voice_id, urls) in enumerate(PROVEN_VOICES):
        elapsed = time.time() - start_time
        
        # Hard time limit for Railway
        if elapsed > 420:  # 7 minutes
            print(f"Time limit reached at {elapsed:.1f}s")
            break
            
        print(f"\n[{i+1}/{len(PROVEN_VOICES)}] Downloading...")
        
        if download_voice_optimized(voice_id, urls):
            total_downloaded += 1
            print(f"  SUCCESS: {voice_id} ({total_downloaded} total)")
        else:
            print(f"  FAILED: {voice_id}")
        
        # Progress updates
        if total_downloaded % 10 == 0 and total_downloaded > 0:
            rate = total_downloaded / (elapsed / 60)
            print(f"\nProgress: {total_downloaded} voices in {elapsed:.1f}s ({rate:.1f}/min)")
        
        # Achieve target early
        if total_downloaded >= 52:
            print(f"Target exceeded! {total_downloaded} voices achieved in {elapsed:.1f}s")
            break
        
        # Brief pause every 5 downloads
        if i % 5 == 4:
            time.sleep(0.5)
    
    elapsed = time.time() - start_time
    
    print(f"\nFinal Optimized Download Complete!")
    print(f"Voices downloaded: {total_downloaded}")
    print(f"Total time: {elapsed:.1f}s")
    print(f"Rate: {total_downloaded / (elapsed / 60):.1f} voices/min")
    
    # Create summary
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
    
    if total_downloaded >= 50:
        print("TARGET ACHIEVED: 50+ voices successfully downloaded!")
    elif total_downloaded >= 45:
        print("NEAR TARGET: Very close to 50 voice goal!")
    else:
        print("PROGRESS: Significant improvement over baseline!")

if __name__ == "__main__":
    main()
