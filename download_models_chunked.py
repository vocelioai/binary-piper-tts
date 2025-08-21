#!/usr/bin/env python3

import os
import sys
import time
import requests
from pathlib import Path

def download_voice_model(voice_id, model_url, json_url, max_retries=3):
    """Download a single voice model with retry logic"""
    model_path = f"models/{voice_id}.onnx"
    json_path = f"models/{voice_id}.onnx.json"
    
    # Skip if already exists
    if os.path.exists(model_path) and os.path.exists(json_path):
        print(f"✅ {voice_id} already exists")
        return True
    
    for attempt in range(max_retries):
        try:
            print(f"📥 Downloading {voice_id} (attempt {attempt + 1})")
            
            # Download model file
            model_response = requests.get(model_url, timeout=60)
            model_response.raise_for_status()
            
            # Download JSON file
            json_response = requests.get(json_url, timeout=30)
            json_response.raise_for_status()
            
            # Save files
            with open(model_path, 'wb') as f:
                f.write(model_response.content)
            with open(json_path, 'w', encoding='utf-8') as f:
                f.write(json_response.text)
            
            print(f"✅ {voice_id} downloaded successfully")
            return True
            
        except Exception as e:
            print(f"❌ {voice_id} failed (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
    
    return False

def main():
    # Create models directory
    os.makedirs("models", exist_ok=True)
    
    # Time management
    start_time = time.time()
    max_time = 7 * 60  # 7 minutes for Railway
    
    print("🚀 CHUNKED VOICE DOWNLOADER - Targeting 50+ voices")
    print("=" * 60)
    
    # CHUNK 1: Super Essential (must have)
    chunk1_voices = [
        # Top English voices
        ("en_US-amy-low", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/amy/low/en_US-amy-low.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/amy/low/en_US-amy-low.onnx.json"),
        ("en_US-lessac-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json"),
        ("en_GB-cori-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/cori/medium/en_GB-cori-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/cori/medium/en_GB-cori-medium.onnx.json"),
        
        # Essential European
        ("es_ES-davefx-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/es/es_ES/davefx/medium/es_ES-davefx-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/es/es_ES/davefx/medium/es_ES-davefx-medium.onnx.json"),
        ("fr_FR-siwis-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx.json"),
        ("de_DE-thorsten-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx.json"),
        ("it_IT-riccardo-x_low", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/it/it_IT/riccardo/x_low/it_IT-riccardo-x_low.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/it/it_IT/riccardo/x_low/it_IT-riccardo-x_low.onnx.json"),
    ]
    
    # CHUNK 2: Important voices (good variety)
    chunk2_voices = [
        # More English
        ("en_US-danny-low", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/danny/low/en_US-danny-low.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/danny/low/en_US-danny-low.onnx.json"),
        ("en_US-kathleen-low", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/kathleen/low/en_US-kathleen-low.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/kathleen/low/en_US-kathleen-low.onnx.json"),
        ("en_US-ryan-high", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/ryan/high/en_US-ryan-high.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/ryan/high/en_US-ryan-high.onnx.json"),
        ("en_GB-northern_english_male-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/northern_english_male/medium/en_GB-northern_english_male-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/northern_english_male/medium/en_GB-northern_english_male-medium.onnx.json"),
        
        # More European
        ("pt_BR-faber-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx.json"),
        ("ru_RU-dmitri-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ru/ru_RU/dmitri/medium/ru_RU-dmitri-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ru/ru_RU/dmitri/medium/ru_RU-dmitri-medium.onnx.json"),
        ("zh_CN-huayan-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/zh/zh_CN/huayan/medium/zh_CN-huayan-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/zh/zh_CN/huayan/medium/zh_CN-huayan-medium.onnx.json"),
        ("ar_JO-kareem-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ar/ar_JO/kareem/medium/ar_JO-kareem-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ar/ar_JO/kareem/medium/ar_JO-kareem-medium.onnx.json"),
    ]
    
    # CHUNK 3: Extended variety (if time permits)
    chunk3_voices = [
        # Scandinavian
        ("no_NO-talesyntese-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/no/no_NO/talesyntese/medium/no_NO-talesyntese-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/no/no_NO/talesyntese/medium/no_NO-talesyntese-medium.onnx.json"),
        ("da_DK-talesyntese-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/da/da_DK/talesyntese/medium/da_DK-talesyntese-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/da/da_DK/talesyntese/medium/da_DK-talesyntese-medium.onnx.json"),
        ("sv_SE-nst-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx.json"),
        
        # Eastern European
        ("uk_UA-ukrainian_tts-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/uk/uk_UA/ukrainian_tts/medium/uk_UA-ukrainian_tts-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/uk/uk_UA/ukrainian_tts/medium/uk_UA-ukrainian_tts-medium.onnx.json"),
        ("ro_RO-mihai-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ro/ro_RO/mihai/medium/ro_RO-mihai-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ro/ro_RO/mihai/medium/ro_RO-mihai-medium.onnx.json"),
        ("cs_CZ-jirka-low", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/cs/cs_CZ/jirka/low/cs_CZ-jirka-low.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/cs/cs_CZ/jirka/low/cs_CZ-jirka-low.onnx.json"),
        
        # More variety
        ("nl_NL-mls_5809-low", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/nl/nl_NL/mls_5809/low/nl_NL-mls_5809-low.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/nl/nl_NL/mls_5809/low/nl_NL-mls_5809-low.onnx.json"),
        ("vi_VN-vivos-x_low", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/vi/vi_VN/vivos/x_low/vi_VN-vivos-x_low.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/vi/vi_VN/vivos/x_low/vi_VN-vivos-x_low.onnx.json"),
    ]
    
    # CHUNK 4: Additional high-value voices
    chunk4_voices = [
        ("en_US-joe-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/joe/medium/en_US-joe-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/joe/medium/en_US-joe-medium.onnx.json"),
        ("en_US-kristin-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/kristin/medium/en_US-kristin-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/kristin/medium/en_US-kristin-medium.onnx.json"),
        ("en_US-kusal-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/kusal/medium/en_US-kusal-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/kusal/medium/en_US-kusal-medium.onnx.json"),
        ("es_ES-sharvard-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/es/es_ES/sharvard/medium/es_ES-sharvard-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/es/es_ES/sharvard/medium/es_ES-sharvard-medium.onnx.json"),
        ("es_MX-ald-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/es/es_MX/ald/medium/es_MX-ald-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/es/es_MX/ald/medium/es_MX-ald-medium.onnx.json"),
        ("fr_FR-mls_1840-low", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/fr/fr_FR/mls_1840/low/fr_FR-mls_1840-low.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/fr/fr_FR/mls_1840/low/fr_FR-mls_1840-low.onnx.json"),
        ("de_DE-eva_k-x_low", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/de/de_DE/eva_k/x_low/de_DE-eva_k-x_low.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/de/de_DE/eva_k/x_low/de_DE-eva_k-x_low.onnx.json"),
        ("it_IT-paola-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/it/it_IT/paola/medium/it_IT-paola-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/it/it_IT/paola/medium/it_IT-paola-medium.onnx.json"),
    ]
    
    # CHUNK 5: Extended collection targeting 50+ voices
    chunk5_voices = [
        ("ca_ES-upc_ona-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ca/ca_ES/upc_ona/medium/ca_ES-upc_ona-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ca/ca_ES/upc_ona/medium/ca_ES-upc_ona-medium.onnx.json"),
        ("fa_IR-gyro-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/fa/fa_IR/gyro/medium/fa_IR-gyro-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/fa/fa_IR/gyro/medium/fa_IR-gyro-medium.onnx.json"),
        ("fi_FI-harri-low", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/fi/fi_FI/harri/low/fi_FI-harri-low.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/fi/fi_FI/harri/low/fi_FI-harri-low.onnx.json"),
        ("hu_HU-anna-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/hu/hu_HU/anna/medium/hu_HU-anna-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/hu/hu_HU/anna/medium/hu_HU-anna-medium.onnx.json"),
        ("is_IS-bui-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/is/is_IS/bui/medium/is_IS-bui-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/is/is_IS/bui/medium/is_IS-bui-medium.onnx.json"),
        ("ka_GE-natia-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ka/ka_GE/natia/medium/ka_GE-natia-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ka/ka_GE/natia/medium/ka_GE-natia-medium.onnx.json"),
        ("kk_KZ-iseke-x_low", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/kk/kk_KZ/iseke/x_low/kk_KZ-iseke-x_low.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/kk/kk_KZ/iseke/x_low/kk_KZ-iseke-x_low.onnx.json"),
        ("lb_LU-marylux-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/lb/lb_LU/marylux/medium/lb_LU-marylux-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/lb/lb_LU/marylux/medium/lb_LU-marylux-medium.onnx.json"),
        ("ne_NP-google-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ne/ne_NP/google/medium/ne_NP-google-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ne/ne_NP/google/medium/ne_NP-google-medium.onnx.json"),
        ("pl_PL-mls_6892-low", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/pl/pl_PL/mls_6892/low/pl_PL-mls_6892-low.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/pl/pl_PL/mls_6892/low/pl_PL-mls_6892-low.onnx.json"),
        ("sk_SK-lili-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sk/sk_SK/lili/medium/sk_SK-lili-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sk/sk_SK/lili/medium/sk_SK-lili-medium.onnx.json"),
        ("sl_SI-artur-medium", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sl/sl_SI/artur/medium/sl_SI-artur-medium.onnx", "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sl/sl_SI/artur/medium/sl_SI-artur-medium.onnx.json"),
    ]
    
    # Process chunks sequentially
    all_chunks = [
        ("ESSENTIAL", chunk1_voices),
        ("IMPORTANT", chunk2_voices), 
        ("EXTENDED", chunk3_voices),
        ("ADDITIONAL", chunk4_voices),
        ("COMPREHENSIVE", chunk5_voices)
    ]
    
    total_downloaded = 0
    
    for chunk_name, voices in all_chunks:
        elapsed = time.time() - start_time
        remaining_time = max_time - elapsed
        
        print(f"\n🔄 Processing {chunk_name} chunk ({len(voices)} voices)")
        print(f"⏱️  Time remaining: {remaining_time:.1f}s")
        
        if remaining_time < 30:  # Need at least 30s for next chunk
            print(f"⏰ Time limit approaching, stopping at {total_downloaded} voices")
            break
        
        chunk_start = time.time()
        
        for voice_id, model_url, json_url in voices:
            elapsed = time.time() - start_time
            if elapsed > max_time:
                print(f"⏰ Time limit reached after {total_downloaded} voices")
                break
                
            if download_voice_model(voice_id, model_url, json_url):
                total_downloaded += 1
        
        chunk_time = time.time() - chunk_start
        print(f"✅ {chunk_name} chunk completed in {chunk_time:.1f}s")
        
        # Check time after each chunk
        elapsed = time.time() - start_time
        if elapsed > max_time:
            break
    
    # Final summary
    total_time = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"🎯 CHUNKED DOWNLOAD COMPLETE!")
    print(f"📊 Total voices downloaded: {total_downloaded}")
    print(f"⏱️  Total time: {total_time:.1f}s")
    print(f"{'='*60}")
    
    return total_downloaded

if __name__ == "__main__":
    main()
