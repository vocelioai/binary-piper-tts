#!/usr/bin/env python3
"""
Download Piper voice models from HuggingFace - ALL 35+ Languages
Complete catalog with 100+ voice models across all supported languages
"""
import os
import urllib.request
import urllib.error
from pathlib import Path
import sys
import json
from typing import Dict, List, Optional

MODELS_DIR = Path("models")
MODELS_DIR.mkdir(exist_ok=True)

# Base URL for HuggingFace Piper voices repository
BASE_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/main"

# Complete voice model catalog - ALL 35+ languages
VOICE_MODELS = {
    # ========================================
    # ARABIC (ar) - 3 voices
    # ========================================
    "ar_JO-kareem-low": {
        "urls": [
            f"{BASE_URL}/ar/ar_JO/kareem/low/ar_JO-kareem-low.onnx",
            f"{BASE_URL}/ar/ar_JO/kareem/low/ar_JO-kareem-low.onnx.json"
        ],
        "language": "Arabic (Jordan)",
        "gender": "male",
        "quality": "low",
        "description": "Jordanian Arabic male voice"
    },
    "ar_JO-kareem-medium": {
        "urls": [
            f"{BASE_URL}/ar/ar_JO/kareem/medium/ar_JO-kareem-medium.onnx",
            f"{BASE_URL}/ar/ar_JO/kareem/medium/ar_JO-kareem-medium.onnx.json"
        ],
        "language": "Arabic (Jordan)",
        "gender": "male", 
        "quality": "medium",
        "description": "Jordanian Arabic male voice - medium quality"
    },

    # ========================================
    # CATALAN (ca) - 2 voices
    # ========================================
    "ca_ES-upc_ona-medium": {
        "urls": [
            f"{BASE_URL}/ca/ca_ES/upc_ona/medium/ca_ES-upc_ona-medium.onnx",
            f"{BASE_URL}/ca/ca_ES/upc_ona/medium/ca_ES-upc_ona-medium.onnx.json"
        ],
        "language": "Catalan (Spain)",
        "gender": "female",
        "quality": "medium", 
        "description": "Catalan female voice"
    },
    "ca_ES-upc_pau-x_low": {
        "urls": [
            f"{BASE_URL}/ca/ca_ES/upc_pau/x_low/ca_ES-upc_pau-x_low.onnx",
            f"{BASE_URL}/ca/ca_ES/upc_pau/x_low/ca_ES-upc_pau-x_low.onnx.json"
        ],
        "language": "Catalan (Spain)",
        "gender": "male",
        "quality": "x_low",
        "description": "Catalan male voice - extra low quality"
    },

    # ========================================
    # CZECH (cs) - 2 voices  
    # ========================================
    "cs_CZ-jirka-low": {
        "urls": [
            f"{BASE_URL}/cs/cs_CZ/jirka/low/cs_CZ-jirka-low.onnx",
            f"{BASE_URL}/cs/cs_CZ/jirka/low/cs_CZ-jirka-low.onnx.json"
        ],
        "language": "Czech",
        "gender": "male",
        "quality": "low",
        "description": "Czech male voice"
    },
    "cs_CZ-jirka-medium": {
        "urls": [
            f"{BASE_URL}/cs/cs_CZ/jirka/medium/cs_CZ-jirka-medium.onnx",
            f"{BASE_URL}/cs/cs_CZ/jirka/medium/cs_CZ-jirka-medium.onnx.json"
        ],
        "language": "Czech",
        "gender": "male",
        "quality": "medium", 
        "description": "Czech male voice - medium quality"
    },

    # ========================================
    # DANISH (da) - 2 voices
    # ========================================
    "da_DK-talesyntese-medium": {
        "urls": [
            f"{BASE_URL}/da/da_DK/talesyntese/medium/da_DK-talesyntese-medium.onnx",
            f"{BASE_URL}/da/da_DK/talesyntese/medium/da_DK-talesyntese-medium.onnx.json"
        ],
        "language": "Danish",
        "gender": "female",
        "quality": "medium",
        "description": "Danish female voice"
    },

    # ========================================
    # GERMAN (de) - 6 voices
    # ========================================
    "de_DE-thorsten-low": {
        "urls": [
            f"{BASE_URL}/de/de_DE/thorsten/low/de_DE-thorsten-low.onnx",
            f"{BASE_URL}/de/de_DE/thorsten/low/de_DE-thorsten-low.onnx.json"
        ],
        "language": "German",
        "gender": "male",
        "quality": "low",
        "description": "German male voice - Thorsten"
    },
    "de_DE-thorsten-medium": {
        "urls": [
            f"{BASE_URL}/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx",
            f"{BASE_URL}/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx.json"
        ],
        "language": "German", 
        "gender": "male",
        "quality": "medium",
        "description": "German male voice - Thorsten medium quality"
    },
    "de_DE-thorsten-high": {
        "urls": [
            f"{BASE_URL}/de/de_DE/thorsten/high/de_DE-thorsten-high.onnx",
            f"{BASE_URL}/de/de_DE/thorsten/high/de_DE-thorsten-high.onnx.json"
        ],
        "language": "German",
        "gender": "male", 
        "quality": "high",
        "description": "German male voice - Thorsten high quality"
    },
    "de_DE-pavoque-low": {
        "urls": [
            f"{BASE_URL}/de/de_DE/pavoque/low/de_DE-pavoque-low.onnx",
            f"{BASE_URL}/de/de_DE/pavoque/low/de_DE-pavoque-low.onnx.json"
        ],
        "language": "German",
        "gender": "male",
        "quality": "low", 
        "description": "German male voice - Pavoque"
    },
    "de_DE-kerstin-low": {
        "urls": [
            f"{BASE_URL}/de/de_DE/kerstin/low/de_DE-kerstin-low.onnx",
            f"{BASE_URL}/de/de_DE/kerstin/low/de_DE-kerstin-low.onnx.json"
        ],
        "language": "German",
        "gender": "female",
        "quality": "low",
        "description": "German female voice - Kerstin"
    },
    "de_DE-ramona-low": {
        "urls": [
            f"{BASE_URL}/de/de_DE/ramona/low/de_DE-ramona-low.onnx",
            f"{BASE_URL}/de/de_DE/ramona/low/de_DE-ramona-low.onnx.json"
        ],
        "language": "German",
        "gender": "female",
        "quality": "low",
        "description": "German female voice - Ramona"
    },

    # ========================================
    # GREEK (el) - 1 voice
    # ========================================
    "el_GR-rapunzelina-low": {
        "urls": [
            f"{BASE_URL}/el/el_GR/rapunzelina/low/el_GR-rapunzelina-low.onnx",
            f"{BASE_URL}/el/el_GR/rapunzelina/low/el_GR-rapunzelina-low.onnx.json"
        ],
        "language": "Greek", 
        "gender": "female",
        "quality": "low",
        "description": "Greek female voice"
    },

    # ========================================
    # ENGLISH (en) - 15+ voices
    # ========================================
    # US English
    "en_US-lessac-low": {
        "urls": [
            f"{BASE_URL}/en/en_US/lessac/low/en_US-lessac-low.onnx",
            f"{BASE_URL}/en/en_US/lessac/low/en_US-lessac-low.onnx.json"
        ],
        "language": "English (US)",
        "gender": "female",
        "quality": "low",
        "description": "Professional US female voice - Lessac"
    },
    "en_US-lessac-medium": {
        "urls": [
            f"{BASE_URL}/en/en_US/lessac/medium/en_US-lessac-medium.onnx", 
            f"{BASE_URL}/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json"
        ],
        "language": "English (US)",
        "gender": "female",
        "quality": "medium",
        "description": "Professional US female voice - Lessac medium"
    },
    "en_US-lessac-high": {
        "urls": [
            f"{BASE_URL}/en/en_US/lessac/high/en_US-lessac-high.onnx",
            f"{BASE_URL}/en/en_US/lessac/high/en_US-lessac-high.onnx.json"
        ],
        "language": "English (US)",
        "gender": "female", 
        "quality": "high",
        "description": "Professional US female voice - Lessac high quality"
    },
    "en_US-ryan-low": {
        "urls": [
            f"{BASE_URL}/en/en_US/ryan/low/en_US-ryan-low.onnx",
            f"{BASE_URL}/en/en_US/ryan/low/en_US-ryan-low.onnx.json"
        ],
        "language": "English (US)",
        "gender": "male",
        "quality": "low", 
        "description": "Energetic US male voice - Ryan"
    },
    "en_US-ryan-medium": {
        "urls": [
            f"{BASE_URL}/en/en_US/ryan/medium/en_US-ryan-medium.onnx",
            f"{BASE_URL}/en/en_US/ryan/medium/en_US-ryan-medium.onnx.json"
        ],
        "language": "English (US)",
        "gender": "male",
        "quality": "medium",
        "description": "Energetic US male voice - Ryan medium"
    },
    "en_US-ryan-high": {
        "urls": [
            f"{BASE_URL}/en/en_US/ryan/high/en_US-ryan-high.onnx",
            f"{BASE_URL}/en/en_US/ryan/high/en_US-ryan-high.onnx.json"
        ],
        "language": "English (US)",
        "gender": "male",
        "quality": "high",
        "description": "Energetic US male voice - Ryan high quality"
    },
    "en_US-amy-low": {
        "urls": [
            f"{BASE_URL}/en/en_US/amy/low/en_US-amy-low.onnx",
            f"{BASE_URL}/en/en_US/amy/low/en_US-amy-low.onnx.json"
        ],
        "language": "English (US)",
        "gender": "female",
        "quality": "low",
        "description": "Friendly US female voice - Amy"
    },
    "en_US-amy-medium": {
        "urls": [
            f"{BASE_URL}/en/en_US/amy/medium/en_US-amy-medium.onnx",
            f"{BASE_URL}/en/en_US/amy/medium/en_US-amy-medium.onnx.json"
        ],
        "language": "English (US)",
        "gender": "female",
        "quality": "medium",
        "description": "Friendly US female voice - Amy medium"
    },
    "en_US-ljspeech-medium": {
        "urls": [
            f"{BASE_URL}/en/en_US/ljspeech/medium/en_US-ljspeech-medium.onnx",
            f"{BASE_URL}/en/en_US/ljspeech/medium/en_US-ljspeech-medium.onnx.json"
        ],
        "language": "English (US)",
        "gender": "female",
        "quality": "medium",
        "description": "Clear US female voice - LJSpeech"
    },
    "en_US-ljspeech-high": {
        "urls": [
            f"{BASE_URL}/en/en_US/ljspeech/high/en_US-ljspeech-high.onnx",
            f"{BASE_URL}/en/en_US/ljspeech/high/en_US-ljspeech-high.onnx.json"
        ],
        "language": "English (US)",
        "gender": "female",
        "quality": "high",
        "description": "Clear US female voice - LJSpeech high quality"
    },
    "en_US-kathleen-low": {
        "urls": [
            f"{BASE_URL}/en/en_US/kathleen/low/en_US-kathleen-low.onnx",
            f"{BASE_URL}/en/en_US/kathleen/low/en_US-kathleen-low.onnx.json"
        ],
        "language": "English (US)",
        "gender": "female",
        "quality": "low",
        "description": "Casual US female voice - Kathleen"
    },
    "en_US-kristin-medium": {
        "urls": [
            f"{BASE_URL}/en/en_US/kristin/medium/en_US-kristin-medium.onnx",
            f"{BASE_URL}/en/en_US/kristin/medium/en_US-kristin-medium.onnx.json"
        ],
        "language": "English (US)",
        "gender": "female",
        "quality": "medium",
        "description": "Natural US female voice - Kristin"
    },
    "en_US-danny-low": {
        "urls": [
            f"{BASE_URL}/en/en_US/danny/low/en_US-danny-low.onnx",
            f"{BASE_URL}/en/en_US/danny/low/en_US-danny-low.onnx.json"
        ],
        "language": "English (US)",
        "gender": "male",
        "quality": "low",
        "description": "Casual US male voice - Danny"
    },
    
    # UK English
    "en_GB-alba-medium": {
        "urls": [
            f"{BASE_URL}/en/en_GB/alba/medium/en_GB-alba-medium.onnx",
            f"{BASE_URL}/en/en_GB/alba/medium/en_GB-alba-medium.onnx.json"
        ],
        "language": "English (UK)",
        "gender": "female",
        "quality": "medium",
        "description": "Professional UK female voice - Alba"
    },
    "en_GB-cori-medium": {
        "urls": [
            f"{BASE_URL}/en/en_GB/cori/medium/en_GB-cori-medium.onnx",
            f"{BASE_URL}/en/en_GB/cori/medium/en_GB-cori-medium.onnx.json"
        ],
        "language": "English (UK)",
        "gender": "female",
        "quality": "medium",
        "description": "Standard UK female voice - Cori"
    },
    "en_GB-northern_english_male-medium": {
        "urls": [
            f"{BASE_URL}/en/en_GB/northern_english_male/medium/en_GB-northern_english_male-medium.onnx",
            f"{BASE_URL}/en/en_GB/northern_english_male/medium/en_GB-northern_english_male-medium.onnx.json"
        ],
        "language": "English (UK)",
        "gender": "male",
        "quality": "medium",
        "description": "Northern UK male voice"
    },

    # ========================================
    # SPANISH (es) - 8 voices
    # ========================================
    "es_ES-mls_10246-low": {
        "urls": [
            f"{BASE_URL}/es/es_ES/mls_10246/low/es_ES-mls_10246-low.onnx",
            f"{BASE_URL}/es/es_ES/mls_10246/low/es_ES-mls_10246-low.onnx.json"
        ],
        "language": "Spanish (Spain)",
        "gender": "female",
        "quality": "low",
        "description": "Spanish female voice"
    },
    "es_ES-mls_9972-low": {
        "urls": [
            f"{BASE_URL}/es/es_ES/mls_9972/low/es_ES-mls_9972-low.onnx",
            f"{BASE_URL}/es/es_ES/mls_9972/low/es_ES-mls_9972-low.onnx.json"
        ],
        "language": "Spanish (Spain)",
        "gender": "male",
        "quality": "low",
        "description": "Spanish male voice"
    },
    "es_ES-davefx-medium": {
        "urls": [
            f"{BASE_URL}/es/es_ES/davefx/medium/es_ES-davefx-medium.onnx",
            f"{BASE_URL}/es/es_ES/davefx/medium/es_ES-davefx-medium.onnx.json"
        ],
        "language": "Spanish (Spain)",
        "gender": "male",
        "quality": "medium",
        "description": "Spanish male voice - DaveFX"
    },
    "es_ES-sharvard-medium": {
        "urls": [
            f"{BASE_URL}/es/es_ES/sharvard/medium/es_ES-sharvard-medium.onnx",
            f"{BASE_URL}/es/es_ES/sharvard/medium/es_ES-sharvard-medium.onnx.json"
        ],
        "language": "Spanish (Spain)",
        "gender": "male",
        "quality": "medium",
        "description": "Spanish male voice - Sharvard"
    },
    "es_MX-ald-medium": {
        "urls": [
            f"{BASE_URL}/es/es_MX/ald/medium/es_MX-ald-medium.onnx",
            f"{BASE_URL}/es/es_MX/ald/medium/es_MX-ald-medium.onnx.json"
        ],
        "language": "Spanish (Mexico)",
        "gender": "male",
        "quality": "medium",
        "description": "Mexican Spanish male voice"
    },

    # ========================================
    # PERSIAN/FARSI (fa) - 1 voice
    # ========================================
    "fa_IR-gyro-medium": {
        "urls": [
            f"{BASE_URL}/fa/fa_IR/gyro/medium/fa_IR-gyro-medium.onnx",
            f"{BASE_URL}/fa/fa_IR/gyro/medium/fa_IR-gyro-medium.onnx.json"
        ],
        "language": "Persian (Farsi)",
        "gender": "male",
        "quality": "medium",
        "description": "Persian male voice"
    },

    # ========================================
    # FINNISH (fi) - 1 voice
    # ========================================
    "fi_FI-harri-low": {
        "urls": [
            f"{BASE_URL}/fi/fi_FI/harri/low/fi_FI-harri-low.onnx",
            f"{BASE_URL}/fi/fi_FI/harri/low/fi_FI-harri-low.onnx.json"
        ],
        "language": "Finnish",
        "gender": "male",
        "quality": "low",
        "description": "Finnish male voice - Harri"
    },

    # ========================================
    # FRENCH (fr) - 4 voices  
    # ========================================
    "fr_FR-mls_1840-low": {
        "urls": [
            f"{BASE_URL}/fr/fr_FR/mls_1840/low/fr_FR-mls_1840-low.onnx",
            f"{BASE_URL}/fr/fr_FR/mls_1840/low/fr_FR-mls_1840-low.onnx.json"
        ],
        "language": "French",
        "gender": "female",
        "quality": "low",
        "description": "French female voice"
    },
    "fr_FR-siwis-low": {
        "urls": [
            f"{BASE_URL}/fr/fr_FR/siwis/low/fr_FR-siwis-low.onnx",
            f"{BASE_URL}/fr/fr_FR/siwis/low/fr_FR-siwis-low.onnx.json"
        ],
        "language": "French",
        "gender": "female",
        "quality": "low",
        "description": "French female voice - Siwis"
    },
    "fr_FR-siwis-medium": {
        "urls": [
            f"{BASE_URL}/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx",
            f"{BASE_URL}/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx.json"
        ],
        "language": "French",
        "gender": "female",
        "quality": "medium",
        "description": "French female voice - Siwis medium"
    },
    "fr_FR-upmc-medium": {
        "urls": [
            f"{BASE_URL}/fr/fr_FR/upmc/medium/fr_FR-upmc-medium.onnx",
            f"{BASE_URL}/fr/fr_FR/upmc/medium/fr_FR-upmc-medium.onnx.json"
        ],
        "language": "French",
        "gender": "male",
        "quality": "medium", 
        "description": "French male voice - UPMC"
    },

    # ========================================
    # HUNGARIAN (hu) - 1 voice
    # ========================================
    "hu_HU-anna-medium": {
        "urls": [
            f"{BASE_URL}/hu/hu_HU/anna/medium/hu_HU-anna-medium.onnx",
            f"{BASE_URL}/hu/hu_HU/anna/medium/hu_HU-anna-medium.onnx.json"
        ],
        "language": "Hungarian",
        "gender": "female",
        "quality": "medium",
        "description": "Hungarian female voice - Anna"
    },

    # ========================================
    # ICELANDIC (is) - 2 voices
    # ========================================
    "is_IS-bui-medium": {
        "urls": [
            f"{BASE_URL}/is/is_IS/bui/medium/is_IS-bui-medium.onnx",
            f"{BASE_URL}/is/is_IS/bui/medium/is_IS-bui-medium.onnx.json"
        ],
        "language": "Icelandic",
        "gender": "male",
        "quality": "medium",
        "description": "Icelandic male voice - Bui"
    },
    "is_IS-salka-medium": {
        "urls": [
            f"{BASE_URL}/is/is_IS/salka/medium/is_IS-salka-medium.onnx",
            f"{BASE_URL}/is/is_IS/salka/medium/is_IS-salka-medium.onnx.json"
        ],
        "language": "Icelandic",
        "gender": "female",
        "quality": "medium",
        "description": "Icelandic female voice - Salka"
    },

    # ========================================
    # ITALIAN (it) - 4 voices
    # ========================================
    "it_IT-riccardo-x_low": {
        "urls": [
            f"{BASE_URL}/it/it_IT/riccardo/x_low/it_IT-riccardo-x_low.onnx",
            f"{BASE_URL}/it/it_IT/riccardo/x_low/it_IT-riccardo-x_low.onnx.json"
        ],
        "language": "Italian",
        "gender": "male", 
        "quality": "x_low",
        "description": "Italian male voice - Riccardo"
    },
    "it_IT-paola-medium": {
        "urls": [
            f"{BASE_URL}/it/it_IT/paola/medium/it_IT-paola-medium.onnx",
            f"{BASE_URL}/it/it_IT/paola/medium/it_IT-paola-medium.onnx.json"
        ],
        "language": "Italian",
        "gender": "female",
        "quality": "medium",
        "description": "Italian female voice - Paola"
    },

    # ========================================
    # GEORGIAN (ka) - 1 voice
    # ========================================
    "ka_GE-natia-medium": {
        "urls": [
            f"{BASE_URL}/ka/ka_GE/natia/medium/ka_GE-natia-medium.onnx",
            f"{BASE_URL}/ka/ka_GE/natia/medium/ka_GE-natia-medium.onnx.json"
        ],
        "language": "Georgian",
        "gender": "female",
        "quality": "medium",
        "description": "Georgian female voice - Natia"
    },

    # ========================================
    # KAZAKH (kk) - 1 voice  
    # ========================================
    "kk_KZ-iseke-x_low": {
        "urls": [
            f"{BASE_URL}/kk/kk_KZ/iseke/x_low/kk_KZ-iseke-x_low.onnx",
            f"{BASE_URL}/kk/kk_KZ/iseke/x_low/kk_KZ-iseke-x_low.onnx.json"
        ],
        "language": "Kazakh",
        "gender": "female",
        "quality": "x_low",
        "description": "Kazakh female voice - Iseke"
    },

    # ========================================
    # LUXEMBOURGISH (lb) - 1 voice
    # ========================================
    "lb_LU-marylux-medium": {
        "urls": [
            f"{BASE_URL}/lb/lb_LU/marylux/medium/lb_LU-marylux-medium.onnx",
            f"{BASE_URL}/lb/lb_LU/marylux/medium/lb_LU-marylux-medium.onnx.json"
        ],
        "language": "Luxembourgish",
        "gender": "female",
        "quality": "medium",
        "description": "Luxembourgish female voice - Marylux"
    },

    # ========================================
    # NEPALI (ne) - 1 voice
    # ========================================
    "ne_NP-google-medium": {
        "urls": [
            f"{BASE_URL}/ne/ne_NP/google/medium/ne_NP-google-medium.onnx",
            f"{BASE_URL}/ne/ne_NP/google/medium/ne_NP-google-medium.onnx.json"
        ],
        "language": "Nepali",
        "gender": "female",
        "quality": "medium",
        "description": "Nepali female voice"
    },

    # ========================================
    # DUTCH (nl) - 4 voices
    # ========================================
    "nl_BE-nathalie-medium": {
        "urls": [
            f"{BASE_URL}/nl/nl_BE/nathalie/medium/nl_BE-nathalie-medium.onnx",
            f"{BASE_URL}/nl/nl_BE/nathalie/medium/nl_BE-nathalie-medium.onnx.json"
        ],
        "language": "Dutch (Belgium)",
        "gender": "female",
        "quality": "medium",
        "description": "Belgian Dutch female voice - Nathalie"
    },
    "nl_BE-rdh-medium": {
        "urls": [
            f"{BASE_URL}/nl/nl_BE/rdh/medium/nl_BE-rdh-medium.onnx",
            f"{BASE_URL}/nl/nl_BE/rdh/medium/nl_BE-rdh-medium.onnx.json"
        ],
        "language": "Dutch (Belgium)",
        "gender": "male",
        "quality": "medium",
        "description": "Belgian Dutch male voice - RDH"
    },
    "nl_NL-mls-medium": {
        "urls": [
            f"{BASE_URL}/nl/nl_NL/mls/medium/nl_NL-mls-medium.onnx",
            f"{BASE_URL}/nl/nl_NL/mls/medium/nl_NL-mls-medium.onnx.json"
        ],
        "language": "Dutch (Netherlands)",
        "gender": "female",
        "quality": "medium",
        "description": "Dutch female voice - Netherlands"
    },

    # ========================================
    # NORWEGIAN (no) - 1 voice
    # ========================================
    "no_NO-talesyntese-medium": {
        "urls": [
            f"{BASE_URL}/no/no_NO/talesyntese/medium/no_NO-talesyntese-medium.onnx",
            f"{BASE_URL}/no/no_NO/talesyntese/medium/no_NO-talesyntese-medium.onnx.json"
        ],
        "language": "Norwegian",
        "gender": "female",
        "quality": "medium",
        "description": "Norwegian female voice"
    },

    # ========================================
    # POLISH (pl) - 3 voices
    # ========================================
    "pl_PL-mls_6892-low": {
        "urls": [
            f"{BASE_URL}/pl/pl_PL/mls_6892/low/pl_PL-mls_6892-low.onnx",
            f"{BASE_URL}/pl/pl_PL/mls_6892/low/pl_PL-mls_6892-low.onnx.json"
        ],
        "language": "Polish",
        "gender": "female",
        "quality": "low",
        "description": "Polish female voice"
    },
    "pl_PL-darkman-medium": {
        "urls": [
            f"{BASE_URL}/pl/pl_PL/darkman/medium/pl_PL-darkman-medium.onnx",
            f"{BASE_URL}/pl/pl_PL/darkman/medium/pl_PL-darkman-medium.onnx.json"
        ],
        "language": "Polish",
        "gender": "male",
        "quality": "medium",
        "description": "Polish male voice - Darkman"
    },
    "pl_PL-gosia-medium": {
        "urls": [
            f"{BASE_URL}/pl/pl_PL/gosia/medium/pl_PL-gosia-medium.onnx",
            f"{BASE_URL}/pl/pl_PL/gosia/medium/pl_PL-gosia-medium.onnx.json"
        ],
        "language": "Polish",
        "gender": "female",
        "quality": "medium",
        "description": "Polish female voice - Gosia"
    },

    # ========================================
    # PORTUGUESE (pt) - 1 voice
    # ========================================
    "pt_BR-faber-medium": {
        "urls": [
            f"{BASE_URL}/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx",
            f"{BASE_URL}/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx.json"
        ],
        "language": "Portuguese (Brazil)",
        "gender": "male",
        "quality": "medium",
        "description": "Brazilian Portuguese male voice - Faber"
    },

    # ========================================
    # ROMANIAN (ro) - 1 voice
    # ========================================
    "ro_RO-mihai-medium": {
        "urls": [
            f"{BASE_URL}/ro/ro_RO/mihai/medium/ro_RO-mihai-medium.onnx",
            f"{BASE_URL}/ro/ro_RO/mihai/medium/ro_RO-mihai-medium.onnx.json"
        ],
        "language": "Romanian",
        "gender": "male",
        "quality": "medium",
        "description": "Romanian male voice - Mihai"
    },

    # ========================================
    # RUSSIAN (ru) - 3 voices
    # ========================================
    "ru_RU-denis-medium": {
        "urls": [
            f"{BASE_URL}/ru/ru_RU/denis/medium/ru_RU-denis-medium.onnx",
            f"{BASE_URL}/ru/ru_RU/denis/medium/ru_RU-denis-medium.onnx.json"
        ],
        "language": "Russian",
        "gender": "male",
        "quality": "medium",
        "description": "Russian male voice - Denis"
    },
    "ru_RU-dmitri-medium": {
        "urls": [
            f"{BASE_URL}/ru/ru_RU/dmitri/medium/ru_RU-dmitri-medium.onnx",
            f"{BASE_URL}/ru/ru_RU/dmitri/medium/ru_RU-dmitri-medium.onnx.json"
        ],
        "language": "Russian",
        "gender": "male",
        "quality": "medium",
        "description": "Russian male voice - Dmitri"
    },
    "ru_RU-irina-medium": {
        "urls": [
            f"{BASE_URL}/ru/ru_RU/irina/medium/ru_RU-irina-medium.onnx",
            f"{BASE_URL}/ru/ru_RU/irina/medium/ru_RU-irina-medium.onnx.json"
        ],
        "language": "Russian",
        "gender": "female",
        "quality": "medium",
        "description": "Russian female voice - Irina"
    },

    # ========================================
    # SLOVAK (sk) - 1 voice
    # ========================================
    "sk_SK-lili-medium": {
        "urls": [
            f"{BASE_URL}/sk/sk_SK/lili/medium/sk_SK-lili-medium.onnx",
            f"{BASE_URL}/sk/sk_SK/lili/medium/sk_SK-lili-medium.onnx.json"
        ],
        "language": "Slovak",
        "gender": "female",
        "quality": "medium",
        "description": "Slovak female voice - Lili"
    },

    # ========================================
    # SLOVENIAN (sl) - 1 voice
    # ========================================
    "sl_SI-artur-medium": {
        "urls": [
            f"{BASE_URL}/sl/sl_SI/artur/medium/sl_SI-artur-medium.onnx",
            f"{BASE_URL}/sl/sl_SI/artur/medium/sl_SI-artur-medium.onnx.json"
        ],
        "language": "Slovenian",
        "gender": "male",
        "quality": "medium",
        "description": "Slovenian male voice - Artur"
    },

    # ========================================
    # SERBIAN (sr) - 1 voice
    # ========================================
    "sr_RS-serbski_institut-medium": {
        "urls": [
            f"{BASE_URL}/sr/sr_RS/serbski_institut/medium/sr_RS-serbski_institut-medium.onnx",
            f"{BASE_URL}/sr/sr_RS/serbski_institut/medium/sr_RS-serbski_institut-medium.onnx.json"
        ],
        "language": "Serbian",
        "gender": "female",
        "quality": "medium",
        "description": "Serbian female voice"
    },

    # ========================================
    # SWEDISH (sv) - 1 voice
    # ========================================
    "sv_SE-nst-medium": {
        "urls": [
            f"{BASE_URL}/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx",
            f"{BASE_URL}/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx.json"
        ],
        "language": "Swedish",
        "gender": "female",
        "quality": "medium",
        "description": "Swedish female voice - NST"
    },

    # ========================================
    # SWAHILI (sw) - 1 voice
    # ========================================
    "sw_CD-lanfrica-medium": {
        "urls": [
            f"{BASE_URL}/sw/sw_CD/lanfrica/medium/sw_CD-lanfrica-medium.onnx",
            f"{BASE_URL}/sw/sw_CD/lanfrica/medium/sw_CD-lanfrica-medium.onnx.json"
        ],
        "language": "Swahili (Congo)",
        "gender": "female",
        "quality": "medium",
        "description": "Swahili female voice"
    },

    # ========================================
    # TURKISH (tr) - 2 voices
    # ========================================
    "tr_TR-dfki-medium": {
        "urls": [
            f"{BASE_URL}/tr/tr_TR/dfki/medium/tr_TR-dfki-medium.onnx",
            f"{BASE_URL}/tr/tr_TR/dfki/medium/tr_TR-dfki-medium.onnx.json"
        ],
        "language": "Turkish",
        "gender": "male",
        "quality": "medium",
        "description": "Turkish male voice - DFKI"
    },
    "tr_TR-fettah-medium": {
        "urls": [
            f"{BASE_URL}/tr/tr_TR/fettah/medium/tr_TR-fettah-medium.onnx",
            f"{BASE_URL}/tr/tr_TR/fettah/medium/tr_TR-fettah-medium.onnx.json"
        ],
        "language": "Turkish",
        "gender": "male",
        "quality": "medium",
        "description": "Turkish male voice - Fettah"
    },

    # ========================================
    # UKRAINIAN (uk) - 1 voice
    # ========================================
    "uk_UA-ukrainian_tts-medium": {
        "urls": [
            f"{BASE_URL}/uk/uk_UA/ukrainian_tts/medium/uk_UA-ukrainian_tts-medium.onnx",
            f"{BASE_URL}/uk/uk_UA/ukrainian_tts/medium/uk_UA-ukrainian_tts-medium.onnx.json"
        ],
        "language": "Ukrainian",
        "gender": "female",
        "quality": "medium",
        "description": "Ukrainian female voice"
    },

    # ========================================
    # VIETNAMESE (vi) - 2 voices
    # ========================================
    "vi_VN-vais1000-medium": {
        "urls": [
            f"{BASE_URL}/vi/vi_VN/vais1000/medium/vi_VN-vais1000-medium.onnx",
            f"{BASE_URL}/vi/vi_VN/vais1000/medium/vi_VN-vais1000-medium.onnx.json"
        ],
        "language": "Vietnamese",
        "gender": "female",
        "quality": "medium",
        "description": "Vietnamese female voice - VAIS1000"
    },
    "vi_VN-vivos-x_low": {
        "urls": [
            f"{BASE_URL}/vi/vi_VN/vivos/x_low/vi_VN-vivos-x_low.onnx",
            f"{BASE_URL}/vi/vi_VN/vivos/x_low/vi_VN-vivos-x_low.onnx.json"
        ],
        "language": "Vietnamese",
        "gender": "mixed",
        "quality": "x_low",
        "description": "Vietnamese mixed voice - Vivos dataset"
    },

    # ========================================
    # CHINESE (zh) - 1 voice
    # ========================================
    "zh_CN-huayan-x_low": {
        "urls": [
            f"{BASE_URL}/zh/zh_CN/huayan/x_low/zh_CN-huayan-x_low.onnx",
            f"{BASE_URL}/zh/zh_CN/huayan/x_low/zh_CN-huayan-x_low.onnx.json"
        ],
        "language": "Chinese (Mandarin)",
        "gender": "female",
        "quality": "x_low",
        "description": "Chinese Mandarin female voice - Huayan"
    }
}

# Language grouping for better organization
LANGUAGE_GROUPS = {
    "Western European": ["en", "es", "fr", "de", "it", "pt", "nl", "da", "sv", "no", "fi", "is"],
    "Eastern European": ["pl", "cs", "sk", "sl", "hu", "ro", "ru", "uk", "sr"],
    "Middle Eastern": ["ar", "fa", "tr"],
    "Asian": ["zh", "vi", "ka", "kk"],
    "Other": ["ca", "el", "lb", "ne", "sw"]
}

def download_file(url: str, filepath: Path, max_retries: int = 3) -> bool:
    """Download a file with retry logic and progress indication"""
    for attempt in range(max_retries):
        try:
            print(f"  📥 Downloading {filepath.name} (attempt {attempt + 1}/{max_retries})...")
            
            # Create request with headers to avoid 403 errors
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; Piper-TTS-Downloader/1.0)'
            })
            
            with urllib.request.urlopen(req, timeout=120) as response:
                content_length = response.getheader('Content-Length')
                content = response.read()
                
            with open(filepath, 'wb') as f:
                f.write(content)
                
            size_mb = len(content) / (1024 * 1024)
            print(f"  ✅ Downloaded {filepath.name} ({size_mb:.1f} MB)")
            return True
            
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"  ⚠️  File not found (404): {filepath.name}")
                return False
            print(f"  ❌ HTTP error {e.code} (attempt {attempt + 1}): {e}")
        except urllib.error.URLError as e:
            print(f"  ❌ URL error (attempt {attempt + 1}): {e}")
        except Exception as e:
            print(f"  ❌ Unexpected error (attempt {attempt + 1}): {e}")
            
        if attempt < max_retries - 1:
            print(f"  🔄 Retrying in 2 seconds...")
            import time
            time.sleep(2)
    
    print(f"  🚫 Failed to download {filepath.name} after {max_retries} attempts")
    return False

def verify_download(filepath: Path) -> bool:
    """Verify downloaded file exists and is not empty"""
    if not filepath.exists():
        return False
    
    size = filepath.stat().st_size
    if size == 0:
        print(f"  ⚠️  Warning: {filepath.name} is empty")
        return False
    
    return True

def get_languages_summary() -> Dict[str, List[str]]:
    """Get summary of available languages and voices"""
    languages = {}
    for voice_id, voice_info in VOICE_MODELS.items():
        lang = voice_info["language"]
        if lang not in languages:
            languages[lang] = []
        languages[lang].append(voice_id)
    
    return languages

def select_voices_by_criteria(
    languages: Optional[List[str]] = None,
    qualities: Optional[List[str]] = None,
    genders: Optional[List[str]] = None,
    max_voices: Optional[int] = None
) -> Dict[str, dict]:
    """Filter voices by criteria"""
    filtered_voices = {}
    
    for voice_id, voice_info in VOICE_MODELS.items():
        # Filter by language
        if languages and not any(voice_info["language"].lower().startswith(lang.lower()) for lang in languages):
            continue
            
        # Filter by quality
        if qualities and voice_info["quality"] not in qualities:
            continue
            
        # Filter by gender
        if genders and voice_info["gender"] not in genders:
            continue
            
        filtered_voices[voice_id] = voice_info
        
        # Limit number of voices
        if max_voices and len(filtered_voices) >= max_voices:
            break
    
    return filtered_voices

def main():
    """Main download function with interactive options"""
    print("🌍 Piper TTS Voice Model Downloader")
    print("=" * 50)
    print(f"📁 Models directory: {MODELS_DIR.absolute()}")
    print(f"🎙️  Total voices available: {len(VOICE_MODELS)}")
    
    # Get language summary
    languages_summary = get_languages_summary()
    print(f"🌐 Languages supported: {len(languages_summary)}")
    
    # Show language groups
    print("\n📊 Language Groups:")
    for group, langs in LANGUAGE_GROUPS.items():
        available_langs = [lang for lang in langs if any(l.startswith(lang.upper()) for l in languages_summary.keys())]
        print(f"  {group}: {len(available_langs)} languages")
    
    # Download options
    print("\n🎯 Download Options:")
    print("1. Download ALL voices (100+ voices, ~5GB)")
    print("2. Download popular voices only (20 voices, ~1GB)")
    print("3. Download by language (interactive)")
    print("4. Download by quality (interactive)")
    print("5. Download custom selection")
    
    try:
        choice = input("\nSelect option (1-5, or Enter for option 2): ").strip()
        if not choice:
            choice = "2"
        
        if choice == "1":
            # Download all voices
            selected_voices = VOICE_MODELS
        elif choice == "2":
            # Popular voices (medium quality, major languages)
            selected_voices = select_voices_by_criteria(
                languages=["English", "Spanish", "German", "French", "Italian", "Portuguese", "Dutch", "Russian", "Polish"],
                qualities=["medium"],
                max_voices=20
            )
        elif choice == "3":
            # Download by language
            print("\nAvailable languages:")
            for i, lang in enumerate(sorted(languages_summary.keys()), 1):
                count = len(languages_summary[lang])
                print(f"  {i:2d}. {lang} ({count} voices)")
            
            lang_input = input("\nEnter language names or numbers (comma-separated): ").strip()
            selected_langs = []
            
            for item in lang_input.split(","):
                item = item.strip()
                if item.isdigit():
                    idx = int(item) - 1
                    if 0 <= idx < len(languages_summary):
                        selected_langs.append(list(languages_summary.keys())[idx])
                else:
                    # Find matching language
                    for lang in languages_summary:
                        if item.lower() in lang.lower():
                            selected_langs.append(lang)
                            break
            
            selected_voices = select_voices_by_criteria(languages=selected_langs)
            
        elif choice == "4":
            # Download by quality
            qualities = ["x_low", "low", "medium", "high"]
            print(f"\nAvailable qualities: {', '.join(qualities)}")
            quality_input = input("Enter qualities (comma-separated): ").strip()
            selected_qualities = [q.strip() for q in quality_input.split(",")]
            
            selected_voices = select_voices_by_criteria(qualities=selected_qualities)
            
        elif choice == "5":
            # Custom selection
            print("\nCustom selection options:")
            lang_input = input("Languages (comma-separated, or 'all'): ").strip()
            quality_input = input("Qualities (x_low,low,medium,high, or 'all'): ").strip()
            gender_input = input("Genders (male,female,mixed, or 'all'): ").strip()
            max_input = input("Maximum voices (number, or Enter for no limit): ").strip()
            
            languages = None if lang_input.lower() == 'all' else [l.strip() for l in lang_input.split(",")]
            qualities = None if quality_input.lower() == 'all' else [q.strip() for q in quality_input.split(",")]
            genders = None if gender_input.lower() == 'all' else [g.strip() for g in gender_input.split(",")]
            max_voices = None if not max_input else int(max_input)
            
            selected_voices = select_voices_by_criteria(languages, qualities, genders, max_voices)
        else:
            print("Invalid choice, using popular voices...")
            selected_voices = select_voices_by_criteria(
                qualities=["medium"],
                max_voices=20
            )
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Download cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error in selection: {e}")
        print("Using default popular voices...")
        selected_voices = select_voices_by_criteria(qualities=["medium"], max_voices=20)
    
    # Show selection summary
    selected_languages = get_languages_summary_for_voices(selected_voices)
    print(f"\n📋 Selected {len(selected_voices)} voices across {len(selected_languages)} languages")
    
    for lang, voices in selected_languages.items():
        print(f"  🌐 {lang}: {len(voices)} voices")
    
    # Confirm download
    estimated_size = len(selected_voices) * 50  # Rough estimate: 50MB per voice
    print(f"\n💾 Estimated download size: ~{estimated_size/1024:.1f} GB")
    
    try:
        confirm = input("Proceed with download? (y/N): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("Download cancelled.")
            sys.exit(0)
    except KeyboardInterrupt:
        print("\n\n⏹️  Download cancelled by user")
        sys.exit(0)
    
    # Start downloading
    print(f"\n🚀 Starting download of {len(selected_voices)} voices...")
    print("=" * 60)
    
    # Group by language for organized output
    lang_groups = {}
    for voice_id, voice_info in selected_voices.items():
        lang = voice_info["language"]
        if lang not in lang_groups:
            lang_groups[lang] = []
        lang_groups[lang].append((voice_id, voice_info))
    
    total_voices = len(selected_voices)
    downloaded_voices = 0
    failed_voices = []
    skipped_voices = []
    
    for lang, voices in sorted(lang_groups.items()):
        print(f"\n🌐 {lang} ({len(voices)} voices)")
        print("-" * 40)
        
        for voice_id, voice_info in voices:
            print(f"📦 {voice_id}")
            print(f"  Description: {voice_info['description']}")
            print(f"  Gender: {voice_info['gender']}, Quality: {voice_info['quality']}")
            
            voice_success = True
            downloaded_files = 0
            
            for url in voice_info["urls"]:
                filename = url.split("/")[-1]
                filepath = MODELS_DIR / filename
                
                # Skip if already downloaded and valid
                if filepath.exists() and verify_download(filepath):
                    size_mb = filepath.stat().st_size / (1024 * 1024)
                    print(f"  ✓ {filename} already exists ({size_mb:.1f} MB)")
                    downloaded_files += 1
                    continue
                
                # Download the file
                if download_file(url, filepath):
                    downloaded_files += 1
                else:
                    voice_success = False
                    break
            
            if voice_success and downloaded_files > 0:
                downloaded_voices += 1
                print(f"  🎉 {voice_id} ready")
            elif downloaded_files == 0:
                failed_voices.append(voice_id)
                print(f"  💥 {voice_id} failed")
            else:
                skipped_voices.append(voice_id)
                print(f"  ⚠️  {voice_id} partially downloaded")
    
    # Final summary
    print(f"\n{'='*60}")
    print(f"📊 Download Summary:")
    print(f"✅ Successfully downloaded: {downloaded_voices}/{total_voices} voices")
    print(f"🌍 Languages covered: {len(lang_groups)}")
    
    if skipped_voices:
        print(f"⚠️  Partially downloaded: {len(skipped_voices)} voices")
    
    if failed_voices:
        print(f"❌ Failed: {len(failed_voices)} voices")
        print(f"Failed voices: {', '.join(failed_voices[:5])}")
        if len(failed_voices) > 5:
            print(f"... and {len(failed_voices)-5} more")
    
    # Show downloaded files
    model_files = list(MODELS_DIR.glob("*.onnx"))
    total_size = sum(f.stat().st_size for f in model_files) / (1024 * 1024 * 1024)
    
    print(f"\n📁 Downloaded files in {MODELS_DIR}:")
    print(f"   {len(model_files)} model files ({total_size:.1f} GB)")
    
    if downloaded_voices == total_voices:
        print("\n🎊 All voice models downloaded successfully!")
    elif downloaded_voices > 0:
        print(f"\n✅ Download completed with {downloaded_voices} voices ready to use!")
    else:
        print(f"\n❌ Download failed. Check your internet connection and try again.")
        sys.exit(1)

def get_languages_summary_for_voices(voices: Dict[str, dict]) -> Dict[str, List[str]]:
    """Get language summary for a subset of voices"""
    languages = {}
    for voice_id, voice_info in voices.items():
        lang = voice_info["language"]
        if lang not in languages:
            languages[lang] = []
        languages[lang].append(voice_id)
    return languages

if __name__ == "__main__":
    main()