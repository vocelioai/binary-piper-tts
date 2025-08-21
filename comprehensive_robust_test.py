#!/usr/bin/env python3
"""Comprehensive voice test with better error handling and retries"""

import requests
import json
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import sys

BASE_URL = "http://127.0.0.1:8000"

# Language-specific test phrases
TEST_PHRASES = {
    'ar': 'مرحبا بالعالم، هذا اختبار لنظام تحويل النص إلى كلام',
    'ca': 'Hola món, aquesta és una prova del sistema de text a veu',
    'cs': 'Ahoj světe, toto je test systému převodu textu na řeč',
    'da': 'Hej verden, dette er en test af tekst-til-tale systemet',
    'de': 'Hallo Welt, das ist ein Test des Text-zu-Sprache-Systems',
    'el': 'Γεια σας κόσμε, αυτό είναι ένα τεστ του συστήματος κειμένου σε ομιλία',
    'en': 'Hello world, this is a test of the text to speech system',
    'es': 'Hola mundo, esta es una prueba del sistema de texto a voz',
    'fa': 'سلام دنیا، این یک آزمایش سیستم تبدیل متن به گفتار است',
    'fi': 'Hei maailma, tämä on teksti puheeksi -järjestelmän testi',
    'fr': 'Bonjour le monde, ceci est un test du système de synthèse vocale',
    'hu': 'Helló világ, ez a szövegfelolvasó rendszer tesztje',
    'is': 'Halló heimur, þetta er prúf á texta í tal kerfinu',
    'it': 'Ciao mondo, questo è un test del sistema di sintesi vocale',
    'ka': 'გამარჯობა მსოფლიო, ეს არის ტექსტიდან მეტყველებაზე სისტემის ტესტი',
    'kk': 'Сәлем әлем, бұл мәтінді дауысқа айналдыру жүйесінің сынағы',
    'lb': 'Moien Welt, dëst ass en Test vum Text-zu-Sprooch System',
    'ne': 'नमस्कार संसार, यो पाठ देखि भाषण प्रणालीको परीक्षण हो',
    'nl': 'Hallo wereld, dit is een test van het tekst-naar-spraak systeem',
    'no': 'Hei verden, dette er en test av tekst-til-tale systemet',
    'pl': 'Witaj świecie, to jest test systemu syntezy mowy',
    'pt': 'Olá mundo, este é um teste do sistema de texto para fala',
    'ro': 'Salut lume, acesta este un test al sistemului text în vorbire',
    'ru': 'Привет мир, это тест системы преобразования текста в речь',
    'sk': 'Ahoj svet, toto je test systému prevodu textu na reč',
    'sl': 'Pozdravljen svet, to je test sistema besedilo v govor',
    'sr': 'Здраво свете, ово је тест система за претварање текста у говор',
    'sv': 'Hej världen, detta är ett test av text-till-tal systemet',
    'sw': 'Hujambo dunia, hii ni jaribio la mfumo wa maandishi hadi kusema',
    'tr': 'Merhaba dünya, bu metin okuma sisteminin bir testidir',
    'uk': 'Привіт світ, це тест системи синтезу мовлення',
    'vi': 'Xin chào thế giới, đây là bài kiểm tra hệ thống chuyển văn bản thành giọng nói',
    'zh': '你好世界，这是文本到语音系统的测试'
}

def make_request_with_retry(url, method="GET", data=None, max_retries=3, timeout=30):
    """Make HTTP request with retry logic"""
    for attempt in range(max_retries):
        try:
            if method == "GET":
                response = requests.get(url, timeout=timeout)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=timeout)
            
            return response
            
        except requests.exceptions.ConnectionError as e:
            print(f"   ⚠️  Connection error (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            continue
        except requests.exceptions.Timeout as e:
            print(f"   ⚠️  Timeout error (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            continue
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")
            break
    
    return None

def test_service_health():
    """Test if the TTS service is running and healthy"""
    print("🔍 Testing TTS Service Health...")
    
    response = make_request_with_retry(f"{BASE_URL}/health")
    if response and response.status_code == 200:
        health_data = response.json()
        print(f"✅ Service is healthy: {health_data['status']}")
        print(f"   📊 Voices loaded: {health_data['voices_loaded']}")
        return True, health_data['voices_loaded']
    else:
        print("❌ Service health check failed")
        return False, 0

def get_available_voices():
    """Get list of available voices"""
    print("📋 Getting available voices...")
    
    response = make_request_with_retry(f"{BASE_URL}/voices")
    if response and response.status_code == 200:
        voices = response.json()
        print(f"✅ Retrieved {len(voices)} voices")
        return voices
    else:
        print("❌ Failed to get voices list")
        return []

def get_language_from_voice(voice_name):
    """Extract language code from voice name"""
    if '_' in voice_name:
        return voice_name.split('_')[0]
    elif '-' in voice_name:
        return voice_name.split('-')[0]
    return 'en'  # Default to English

def test_single_voice(voice_name):
    """Test synthesis for a single voice"""
    lang = get_language_from_voice(voice_name)
    test_text = TEST_PHRASES.get(lang, TEST_PHRASES['en'])
    
    result = {
        'voice': voice_name,
        'language': lang,
        'text': test_text,
        'success': False,
        'audio_size': 0,
        'duration_ms': 0,
        'error': None
    }
    
    try:
        start_time = time.time()
        
        synthesis_data = {
            "text": test_text,
            "voice": voice_name
        }
        
        response = make_request_with_retry(
            f"{BASE_URL}/synthesize", 
            method="POST", 
            data=synthesis_data,
            timeout=60
        )
        
        if response and response.status_code == 200:
            duration = int((time.time() - start_time) * 1000)
            audio_size = len(response.content)
            
            result.update({
                'success': True,
                'audio_size': audio_size,
                'duration_ms': duration
            })
            
            # Save audio file
            os.makedirs("test_outputs", exist_ok=True)
            output_file = f"test_outputs/{voice_name}_test.wav"
            with open(output_file, "wb") as f:
                f.write(response.content)
                
        else:
            error_msg = f"HTTP {response.status_code}" if response else "No response"
            result['error'] = error_msg
            
    except Exception as e:
        result['error'] = str(e)
    
    return result

def run_voice_tests(voices, max_workers=5):
    """Run tests for all voices with controlled concurrency"""
    print(f"\n🎯 Testing {len(voices)} voices...")
    print(f"   Using {max_workers} concurrent workers")
    print("=" * 80)
    
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_voice = {executor.submit(test_single_voice, voice): voice for voice in voices}
        
        completed = 0
        for future in as_completed(future_to_voice):
            voice = future_to_voice[future]
            try:
                result = future.result()
                results.append(result)
                
                completed += 1
                if result['success']:
                    print(f"✅ {completed:2d}/{len(voices)} {voice:<35} "
                          f"({result['audio_size']:>6} bytes, {result['duration_ms']:>4}ms)")
                else:
                    print(f"❌ {completed:2d}/{len(voices)} {voice:<35} "
                          f"ERROR: {result['error']}")
                    
            except Exception as e:
                completed += 1
                print(f"❌ {completed:2d}/{len(voices)} {voice:<35} EXCEPTION: {e}")
                results.append({
                    'voice': voice,
                    'success': False,
                    'error': str(e)
                })
    
    return results

def generate_summary_report(results):
    """Generate and save test summary report"""
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    total_voices = len(results)
    success_count = len(successful)
    failure_count = len(failed)
    success_rate = (success_count / total_voices * 100) if total_voices > 0 else 0
    
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    print(f"Total Voices:    {total_voices}")
    print(f"Successful:      {success_count} ({success_rate:.1f}%)")
    print(f"Failed:          {failure_count}")
    
    if successful:
        avg_size = sum(r['audio_size'] for r in successful) / len(successful)
        avg_duration = sum(r['duration_ms'] for r in successful) / len(successful)
        print(f"Average Size:    {avg_size:.0f} bytes")
        print(f"Average Time:    {avg_duration:.0f}ms")
    
    if failed:
        print(f"\n❌ FAILED VOICES:")
        for result in failed:
            print(f"   {result['voice']}: {result.get('error', 'Unknown error')}")
    
    # Language breakdown
    if successful:
        lang_counts = {}
        for result in successful:
            lang = result.get('language', 'unknown')
            lang_counts[lang] = lang_counts.get(lang, 0) + 1
        
        print(f"\n🌍 LANGUAGES TESTED ({len(lang_counts)} languages):")
        for lang, count in sorted(lang_counts.items()):
            print(f"   {lang}: {count} voices")
    
    # Save detailed JSON report
    report_data = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total_voices': total_voices,
            'successful': success_count,
            'failed': failure_count,
            'success_rate': success_rate
        },
        'results': results
    }
    
    with open('comprehensive_test_report.json', 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Detailed report saved: comprehensive_test_report.json")
    return success_rate >= 95  # Consider test passed if 95%+ success rate

def main():
    """Main test execution"""
    print("🚀 COMPREHENSIVE TTS VOICE TESTING")
    print("=" * 80)
    print(f"🕒 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 1: Health check
    is_healthy, voice_count = test_service_health()
    if not is_healthy:
        print("❌ Service is not healthy. Cannot proceed with testing.")
        sys.exit(1)
    
    # Step 2: Get voices
    voices = get_available_voices()
    if not voices:
        print("❌ No voices available for testing.")
        sys.exit(1)
    
    print(f"\n🎭 Found {len(voices)} voices to test")
    
    # Step 3: Run tests
    results = run_voice_tests(voices, max_workers=3)  # Reduced concurrency
    
    # Step 4: Generate report
    success = generate_summary_report(results)
    
    print(f"\n🕒 Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if success:
        print("✅ COMPREHENSIVE TEST PASSED! 🎉")
    else:
        print("⚠️  Some voices failed - check the detailed report")
    
    return 0 if success else 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during testing: {e}")
        sys.exit(1)
