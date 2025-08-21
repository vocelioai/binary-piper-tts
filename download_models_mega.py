#!/usr/bin/env python3

import os
import sys
import time
import requests
from pathlib import Path
import concurrent.futures
from threading import Lock

# Thread-safe counter
download_lock = Lock()
downloaded_count = 0

def download_voice_model(voice_data, max_retries=2):
    """Download a single voice model with optimized retry logic"""
    global downloaded_count
    
    voice_id, model_url, json_url, size_estimate = voice_data
    model_path = f"models/{voice_id}.onnx"
    json_path = f"models/{voice_id}.onnx.json"
    
    # Skip if already exists
    if os.path.exists(model_path) and os.path.exists(json_path):
        with download_lock:
            downloaded_count += 1
        print(f"✅ {voice_id} already exists ({downloaded_count})")
        return True
    
    for attempt in range(max_retries):
        try:
            print(f"📥 {voice_id} ({size_estimate}MB) - attempt {attempt + 1}")
            
            # Download model file with timeout based on size
            timeout = min(120, max(30, size_estimate * 10))  # 10s per MB, max 2min
            model_response = requests.get(model_url, timeout=timeout)
            model_response.raise_for_status()
            
            # Download JSON file
            json_response = requests.get(json_url, timeout=20)
            json_response.raise_for_status()
            
            # Save files atomically
            temp_model = f"{model_path}.tmp"
            temp_json = f"{json_path}.tmp"
            
            with open(temp_model, 'wb') as f:
                f.write(model_response.content)
            with open(temp_json, 'w', encoding='utf-8') as f:
                f.write(json_response.text)
            
            # Atomic rename
            os.rename(temp_model, model_path)
            os.rename(temp_json, json_path)
            
            with download_lock:
                downloaded_count += 1
            
            print(f"✅ {voice_id} downloaded successfully ({downloaded_count})")
            return True
            
        except Exception as e:
            print(f"❌ {voice_id} failed (attempt {attempt + 1}): {str(e)[:100]}")
            if attempt < max_retries - 1:
                time.sleep(1)
    
    return False

def main():
    # Create models directory
    os.makedirs("models", exist_ok=True)
    
    # Time management
    start_time = time.time()
    max_time = 6.5 * 60  # 6.5 minutes for Railway (leave buffer)
    
    print("🚀 MEGA VOICE DOWNLOADER - Targeting 73+ voices")
    print("=" * 60)
    
    # ALL 73+ VOICES - Optimized by size (smallest first for speed)
    all_voices = [
        # TIER 1: Ultra-small voices (x_low quality) - ~2-8MB each
        ("en_US-amy-low", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/amy/low/en_US-amy-low.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/amy/low/en_US-amy-low.onnx.json", 3),
        ("it_IT-riccardo-x_low", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/it/it_IT/riccardo/x_low/it_IT-riccardo-x_low.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/it/it_IT/riccardo/x_low/it_IT-riccardo-x_low.onnx.json", 2),
        ("de_DE-eva_k-x_low", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/de/de_DE/eva_k/x_low/de_DE-eva_k-x_low.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/de/de_DE/eva_k/x_low/de_DE-eva_k-x_low.onnx.json", 2),
        ("vi_VN-vivos-x_low", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/vi/vi_VN/vivos/x_low/vi_VN-vivos-x_low.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/vi/vi_VN/vivos/x_low/vi_VN-vivos-x_low.onnx.json", 2),
        ("kk_KZ-iseke-x_low", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/kk/kk_KZ/iseke/x_low/kk_KZ-iseke-x_low.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/kk/kk_KZ/iseke/x_low/kk_KZ-iseke-x_low.onnx.json", 2),
        
        # TIER 2: Small voices (low quality) - ~5-15MB each
        ("en_US-danny-low", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/danny/low/en_US-danny-low.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/danny/low/en_US-danny-low.onnx.json", 8),
        ("en_US-kathleen-low", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/kathleen/low/en_US-kathleen-low.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/kathleen/low/en_US-kathleen-low.onnx.json", 8),
        ("fr_FR-mls_1840-low", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/fr/fr_FR/mls_1840/low/fr_FR-mls_1840-low.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/fr/fr_FR/mls_1840/low/fr_FR-mls_1840-low.onnx.json", 12),
        ("nl_NL-mls_5809-low", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/nl/nl_NL/mls_5809/low/nl_NL-mls_5809-low.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/nl/nl_NL/mls_5809/low/nl_NL-mls_5809-low.onnx.json", 11),
        ("cs_CZ-jirka-low", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/cs/cs_CZ/jirka/low/cs_CZ-jirka-low.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/cs/cs_CZ/jirka/low/cs_CZ-jirka-low.onnx.json", 9),
        ("pl_PL-mls_6892-low", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/pl/pl_PL/mls_6892/low/pl_PL-mls_6892-low.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/pl/pl_PL/mls_6892/low/pl_PL-mls_6892-low.onnx.json", 10),
        ("el_GR-rapunzelina-low", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/el/el_GR/rapunzelina/low/el_GR-rapunzelina-low.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/el/el_GR/rapunzelina/low/el_GR-rapunzelina-low.onnx.json", 7),
        ("fi_FI-harri-low", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/fi/fi_FI/harri/low/fi_FI-harri-low.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/fi/fi_FI/harri/low/fi_FI-harri-low.onnx.json", 6),
        
        # TIER 3: Essential medium voices - ~15-35MB each  
        ("en_US-lessac-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json", 25),
        ("en_GB-cori-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/cori/medium/en_GB-cori-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/cori/medium/en_GB-cori-medium.onnx.json", 28),
        ("es_ES-davefx-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/es/es_ES/davefx/medium/es_ES-davefx-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/es/es_ES/davefx/medium/es_ES-davefx-medium.onnx.json", 22),
        ("fr_FR-siwis-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx.json", 20),
        ("de_DE-thorsten-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx.json", 32),
        ("it_IT-paola-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/it/it_IT/paola/medium/it_IT-paola-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/it/it_IT/paola/medium/it_IT-paola-medium.onnx.json", 18),
        ("pt_BR-faber-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx.json", 24),
        ("ru_RU-dmitri-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ru/ru_RU/dmitri/medium/ru_RU-dmitri-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ru/ru_RU/dmitri/medium/ru_RU-dmitri-medium.onnx.json", 26),
        ("zh_CN-huayan-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/zh/zh_CN/huayan/medium/zh_CN-huayan-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/zh/zh_CN/huayan/medium/zh_CN-huayan-medium.onnx.json", 19),
        ("ar_JO-kareem-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ar/ar_JO/kareem/medium/ar_JO-kareem-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ar/ar_JO/kareem/medium/ar_JO-kareem-medium.onnx.json", 16),
        
        # TIER 4: More medium voices - continue building variety
        ("es_ES-sharvard-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/es/es_ES/sharvard/medium/es_ES-sharvard-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/es/es_ES/sharvard/medium/es_ES-sharvard-medium.onnx.json", 23),
        ("es_MX-ald-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/es/es_MX/ald/medium/es_MX-ald-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/es/es_MX/ald/medium/es_MX-ald-medium.onnx.json", 21),
        ("en_US-joe-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/joe/medium/en_US-joe-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/joe/medium/en_US-joe-medium.onnx.json", 29),
        ("en_US-kristin-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/kristin/medium/en_US-kristin-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/kristin/medium/en_US-kristin-medium.onnx.json", 27),
        ("en_US-kusal-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/kusal/medium/en_US-kusal-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/kusal/medium/en_US-kusal-medium.onnx.json", 30),
        ("en_GB-alba-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/alba/medium/en_GB-alba-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/alba/medium/en_GB-alba-medium.onnx.json", 26),
        ("en_GB-jenny_dioco-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/jenny_dioco/medium/en_GB-jenny_dioco-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/jenny_dioco/medium/en_GB-jenny_dioco-medium.onnx.json", 25),
        ("en_GB-northern_english_male-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/northern_english_male/medium/en_GB-northern_english_male-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/northern_english_male/medium/en_GB-northern_english_male-medium.onnx.json", 28),
        
        # TIER 5: Scandinavian and Nordic voices
        ("no_NO-talesyntese-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/no/no_NO/talesyntese/medium/no_NO-talesyntese-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/no/no_NO/talesyntese/medium/no_NO-talesyntese-medium.onnx.json", 20),
        ("da_DK-talesyntese-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/da/da_DK/talesyntese/medium/da_DK-talesyntese-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/da/da_DK/talesyntese/medium/da_DK-talesyntese-medium.onnx.json", 19),
        ("sv_SE-nst-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx.json", 18),
        ("is_IS-bui-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/is/is_IS/bui/medium/is_IS-bui-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/is/is_IS/bui/medium/is_IS-bui-medium.onnx.json", 17),
        
        # TIER 6: Eastern European voices
        ("uk_UA-ukrainian_tts-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/uk/uk_UA/ukrainian_tts/medium/uk_UA-ukrainian_tts-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/uk/uk_UA/ukrainian_tts/medium/uk_UA-ukrainian_tts-medium.onnx.json", 22),
        ("ro_RO-mihai-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ro/ro_RO/mihai/medium/ro_RO-mihai-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ro/ro_RO/mihai/medium/ro_RO-mihai-medium.onnx.json", 24),
        ("sk_SK-lili-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sk/sk_SK/lili/medium/sk_SK-lili-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sk/sk_SK/lili/medium/sk_SK-lili-medium.onnx.json", 21),
        ("sl_SI-artur-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sl/sl_SI/artur/medium/sl_SI-artur-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sl/sl_SI/artur/medium/sl_SI-artur-medium.onnx.json", 20),
        ("hu_HU-anna-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/hu/hu_HU/anna/medium/hu_HU-anna-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/hu/hu_HU/anna/medium/hu_HU-anna-medium.onnx.json", 19),
        
        # TIER 7: Additional variety voices
        ("ca_ES-upc_ona-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ca/ca_ES/upc_ona/medium/ca_ES-upc_ona-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ca/ca_ES/upc_ona/medium/ca_ES-upc_ona-medium.onnx.json", 16),
        ("fa_IR-gyro-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/fa/fa_IR/gyro/medium/fa_IR-gyro-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/fa/fa_IR/gyro/medium/fa_IR-gyro-medium.onnx.json", 15),
        ("ka_GE-natia-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ka/ka_GE/natia/medium/ka_GE-natia-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ka/ka_GE/natia/medium/ka_GE-natia-medium.onnx.json", 14),
        ("lb_LU-marylux-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/lb/lb_LU/marylux/medium/lb_LU-marylux-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/lb/lb_LU/marylux/medium/lb_LU-marylux-medium.onnx.json", 13),
        ("ne_NP-google-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ne/ne_NP/google/medium/ne_NP-google-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ne/ne_NP/google/medium/ne_NP-google-medium.onnx.json", 18),
        ("tr_TR-dfki-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/tr/tr_TR/dfki/medium/tr_TR-dfki-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/tr/tr_TR/dfki/medium/tr_TR-dfki-medium.onnx.json", 22),
        
        # TIER 8: High-quality voices (if time permits)
        ("en_US-ryan-high", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/ryan/high/en_US-ryan-high.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/ryan/high/en_US-ryan-high.onnx.json", 45),
        
        # TIER 9: More specialized voices (targeting 50+)
        ("az_AZ-babah-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/az/az_AZ/babah/medium/az_AZ-babah-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/az/az_AZ/babah/medium/az_AZ-babah-medium.onnx.json", 17),
        ("bn_BD-an_habib-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/bn/bn_BD/an_habib/medium/bn_BD-an_habib-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/bn/bn_BD/an_habib/medium/bn_BD-an_habib-medium.onnx.json", 20),
        ("bg_BG-massimo-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/bg/bg_BG/massimo/medium/bg_BG-massimo-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/bg/bg_BG/massimo/medium/bg_BG-massimo-medium.onnx.json", 18),
        ("hr_HR-filip-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/hr/hr_HR/filip/medium/hr_HR-filip-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/hr/hr_HR/filip/medium/hr_HR-filip-medium.onnx.json", 19),
        ("et_EE-alex-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/et/et_EE/alex/medium/et_EE-alex-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/et/et_EE/alex/medium/et_EE-alex-medium.onnx.json", 16),
        ("lv_LV-nora-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/lv/lv_LV/nora/medium/lv_LV-nora-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/lv/lv_LV/nora/medium/lv_LV-nora-medium.onnx.json", 15),
        ("lt_LT-ona-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/lt/lt_LT/ona/medium/lt_LT-ona-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/lt/lt_LT/ona/medium/lt_LT-ona-medium.onnx.json", 17),
        ("mk_MK-darko-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/mk/mk_MK/darko/medium/mk_MK-darko-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/mk/mk_MK/darko/medium/mk_MK-darko-medium.onnx.json", 18),
        ("mt_MT-paul-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/mt/mt_MT/paul/medium/mt_MT-paul-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/mt/mt_MT/paul/medium/mt_MT-paul-medium.onnx.json", 14),
        
        # TIER 10: Extended collection for 60+ voices
        ("sr_RS-serbski-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sr/sr_RS/serbski/medium/sr_RS-serbski-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sr/sr_RS/serbski/medium/sr_RS-serbski-medium.onnx.json", 21),
        ("sw_TZ-lanfrica-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sw/sw_TZ/lanfrica/medium/sw_TZ-lanfrica-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sw/sw_TZ/lanfrica/medium/sw_TZ-lanfrica-medium.onnx.json", 16),
        ("th_TH-kham-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/th/th_TH/kham/medium/th_TH-kham-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/th/th_TH/kham/medium/th_TH-kham-medium.onnx.json", 19),
        ("ur_PK-ameer-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ur/ur_PK/ameer/medium/ur_PK-ameer-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ur/ur_PK/ameer/medium/ur_PK-ameer-medium.onnx.json", 18),
        
        # TIER 11: Additional languages for 70+ target
        ("cy_GB-gwryw-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/cy/cy_GB/gwryw/medium/cy_GB-gwryw-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/cy/cy_GB/gwryw/medium/cy_GB-gwryw-medium.onnx.json", 16),
        ("ga_IE-an_ghaeilge-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ga/ga_IE/an_ghaeilge/medium/ga_IE-an_ghaeilge-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ga/ga_IE/an_ghaeilge/medium/ga_IE-an_ghaeilge-medium.onnx.json", 15),
        ("he_IL-shira-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/he/he_IL/shira/medium/he_IL-shira-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/he/he_IL/shira/medium/he_IL-shira-medium.onnx.json", 17),
        ("hi_IN-keerti-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/hi/hi_IN/keerti/medium/hi_IN-keerti-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/hi/hi_IN/keerti/medium/hi_IN-keerti-medium.onnx.json", 20),
        ("id_ID-irwan-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/id/id_ID/irwan/medium/id_ID-irwan-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/id/id_ID/irwan/medium/id_ID-irwan-medium.onnx.json", 18),
        ("ja_JP-yukiko-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ja/ja_JP/yukiko/medium/ja_JP-yukiko-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ja/ja_JP/yukiko/medium/ja_JP-yukiko-medium.onnx.json", 22),
        ("ko_KR-minji-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ko/ko_KR/minji/medium/ko_KR-minji-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ko/ko_KR/minji/medium/ko_KR-minji-medium.onnx.json", 21),
        ("ms_MY-yasmin-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ms/ms_MY/yasmin/medium/ms_MY-yasmin-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ms/ms_MY/yasmin/medium/ms_MY-yasmin-medium.onnx.json", 19),
        ("ta_IN-aadhira-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ta/ta_IN/aadhira/medium/ta_IN-aadhira-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ta/ta_IN/aadhira/medium/ta_IN-aadhira-medium.onnx.json", 23),
        ("te_IN-kaveri-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/te/te_IN/kaveri/medium/te_IN-kaveri-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/te/te_IN/kaveri/medium/te_IN-kaveri-medium.onnx.json", 24),
        
        # TIER 12: Final push to 73+ voices
        ("gu_IN-aditya-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/gu/gu_IN/aditya/medium/gu_IN-aditya-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/gu/gu_IN/aditya/medium/gu_IN-aditya-medium.onnx.json", 22),
        ("ml_IN-anusree-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ml/ml_IN/anusree/medium/ml_IN-anusree-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ml/ml_IN/anusree/medium/ml_IN-anusree-medium.onnx.json", 25),
        ("kn_IN-raksha-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/kn/kn_IN/raksha/medium/kn_IN-raksha-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/kn/kn_IN/raksha/medium/kn_IN-raksha-medium.onnx.json", 21),
    ]
    
    print(f"🎯 Target: {len(all_voices)} voices")
    
    # Use parallel downloads for speed (but limited to avoid overwhelming)
    max_workers = 3  # Conservative for Railway
    failed_voices = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_voice = {}
        
        for voice_data in all_voices:
            elapsed = time.time() - start_time
            if elapsed > max_time:
                print(f"⏰ Time limit reached, stopping submission of new downloads")
                break
                
            future = executor.submit(download_voice_model, voice_data)
            future_to_voice[future] = voice_data[0]
        
        # Wait for completion with timeout
        for future in concurrent.futures.as_completed(future_to_voice, timeout=max_time):
            voice_id = future_to_voice[future]
            try:
                success = future.result()
                if not success:
                    failed_voices.append(voice_id)
            except Exception as e:
                print(f"❌ {voice_id} exception: {e}")
                failed_voices.append(voice_id)
            
            # Check time limit
            elapsed = time.time() - start_time
            if elapsed > max_time:
                print(f"⏰ Time limit reached during downloads")
                break
    
    # Final summary
    total_time = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"🎯 MEGA DOWNLOAD COMPLETE!")
    print(f"✅ Successfully downloaded: {downloaded_count}")
    if failed_voices:
        print(f"❌ Failed downloads: {len(failed_voices)}")
        print("   Failed voices:", ", ".join(failed_voices[:10]))
    print(f"⏱️  Total time: {total_time:.1f}s")
    print(f"📊 Success rate: {(downloaded_count/(downloaded_count+len(failed_voices))*100):.1f}%")
    print(f"{'='*60}")
    
    return downloaded_count

if __name__ == "__main__":
    main()
