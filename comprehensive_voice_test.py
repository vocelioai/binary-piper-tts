#!/usr/bin/env python3
"""
Comprehensive Binary Piper TTS Service Test Suite
Tests all 73 voices systematically with detailed reporting
"""
import requests
import json
import time
from pathlib import Path
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

BASE_URL = "http://localhost:8000"

# Test phrases for different languages
TEST_PHRASES = {
    "arabic": "مرحبا، هذا اختبار للصوت العربي",
    "catalan": "Hola, aquesta és una prova de veu catalana",
    "chinese": "你好，这是中文语音测试",
    "czech": "Ahoj, toto je test českého hlasu",
    "danish": "Hej, dette er en test af dansk stemme",
    "dutch": "Hallo, dit is een test van Nederlandse stem",
    "english": "Hello, this is a comprehensive voice test!",
    "finnish": "Hei, tämä on suomalaisen äänen testi",
    "french": "Bonjour, ceci est un test de voix française",
    "georgian": "გამარჯობა, ეს არის ქართული ხმის ტესტი",
    "german": "Hallo, dies ist ein Test der deutschen Stimme",
    "greek": "Γεια σας, αυτό είναι ένα τεστ ελληνικής φωνής",
    "hungarian": "Helló, ez egy magyar hang teszt",
    "icelandic": "Halló, þetta er próf á íslenskri röddu",
    "italian": "Ciao, questo è un test della voce italiana",
    "kazakh": "Сәлем, бұл қазақ дауысының сынағы",
    "luxembourgish": "Moien, dëst ass en Test vun der lëtzebuerger Stëmm",
    "nepali": "नमस्ते, यो नेपाली आवाजको परीक्षण हो",
    "norwegian": "Hei, dette er en test av norsk stemme",
    "persian": "سلام، این یک تست صدای فارسی است",
    "polish": "Cześć, to jest test polskiego głosu",
    "portuguese": "Olá, este é um teste de voz portuguesa",
    "romanian": "Salut, acesta este un test de voce română",
    "russian": "Привет, это тест русского голоса",
    "serbian": "Здраво, ово је тест српског гласа",
    "slovak": "Ahoj, toto je test slovenského hlasu",
    "slovenian": "Pozdravljeni, to je test slovenskega glasu",
    "spanish": "Hola, esta es una prueba de voz española",
    "swahili": "Hujambo, huu ni mtihani wa sauti ya Kiswahili",
    "swedish": "Hej, detta är ett test av svensk röst",
    "turkish": "Merhaba, bu Türkçe ses testi",
    "ukrainian": "Привіт, це тест української мови",
    "vietnamese": "Xin chào, đây là bài kiểm tra giọng nói tiếng Việt"
}

def get_language_key(voice_name):
    """Extract language key from voice name for test phrase selection"""
    if voice_name.startswith('ar_'):
        return 'arabic'
    elif voice_name.startswith('ca_'):
        return 'catalan'
    elif voice_name.startswith('zh_'):
        return 'chinese'
    elif voice_name.startswith('cs_'):
        return 'czech'
    elif voice_name.startswith('da_'):
        return 'danish'
    elif voice_name.startswith('nl_'):
        return 'dutch'
    elif voice_name.startswith('en_'):
        return 'english'
    elif voice_name.startswith('fi_'):
        return 'finnish'
    elif voice_name.startswith('fr_'):
        return 'french'
    elif voice_name.startswith('ka_'):
        return 'georgian'
    elif voice_name.startswith('de_'):
        return 'german'
    elif voice_name.startswith('el_'):
        return 'greek'
    elif voice_name.startswith('hu_'):
        return 'hungarian'
    elif voice_name.startswith('is_'):
        return 'icelandic'
    elif voice_name.startswith('it_'):
        return 'italian'
    elif voice_name.startswith('kk_'):
        return 'kazakh'
    elif voice_name.startswith('lb_'):
        return 'luxembourgish'
    elif voice_name.startswith('ne_'):
        return 'nepali'
    elif voice_name.startswith('no_'):
        return 'norwegian'
    elif voice_name.startswith('fa_'):
        return 'persian'
    elif voice_name.startswith('pl_'):
        return 'polish'
    elif voice_name.startswith('pt_'):
        return 'portuguese'
    elif voice_name.startswith('ro_'):
        return 'romanian'
    elif voice_name.startswith('ru_'):
        return 'russian'
    elif voice_name.startswith('sr_'):
        return 'serbian'
    elif voice_name.startswith('sk_'):
        return 'slovak'
    elif voice_name.startswith('sl_'):
        return 'slovenian'
    elif voice_name.startswith('es_'):
        return 'spanish'
    elif voice_name.startswith('sw_'):
        return 'swahili'
    elif voice_name.startswith('sv_'):
        return 'swedish'
    elif voice_name.startswith('tr_'):
        return 'turkish'
    elif voice_name.startswith('uk_'):
        return 'ukrainian'
    elif voice_name.startswith('vi_'):
        return 'vietnamese'
    else:
        return 'english'  # fallback

def test_service_health():
    """Test if the TTS service is running and healthy"""
    print("🔍 Testing TTS Service Health...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Service is healthy: {health_data['status']}")
            print(f"   📊 Voices loaded: {health_data['voices_loaded']}")
            print(f"   🎯 Binary path: {health_data.get('piper_binary', 'Unknown')}")
            return True
        else:
            print(f"❌ Health check failed: HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to service: {e}")
        return False

def get_available_voices():
    """Get list of all available voices"""
    print("\n🎙️ Retrieving Available Voices...")
    try:
        response = requests.get(f"{BASE_URL}/voices", timeout=10)
        if response.status_code == 200:
            voices = response.json()
            print(f"✅ Found {len(voices)} voices available")
            return voices
        else:
            print(f"❌ Failed to get voices: HTTP {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"❌ Error getting voices: {e}")
        return []

def test_single_voice(voice_name, test_num, total_voices):
    """Test synthesis with a single voice"""
    lang_key = get_language_key(voice_name)
    test_text = TEST_PHRASES.get(lang_key, TEST_PHRASES['english'])
    
    print(f"[{test_num:2d}/{total_voices}] Testing {voice_name}...")
    
    try:
        payload = {
            "text": test_text,
            "voice": voice_name
        }
        
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/synthesize",
            json=payload,
            timeout=30,
            headers={"Content-Type": "application/json"}
        )
        synthesis_time = time.time() - start_time
        
        if response.status_code == 200:
            # Save audio file
            output_file = f"test_output/{voice_name}.wav"
            Path("test_output").mkdir(exist_ok=True)
            
            with open(output_file, "wb") as f:
                f.write(response.content)
            
            file_size = Path(output_file).stat().st_size
            
            result = {
                'voice': voice_name,
                'status': 'SUCCESS',
                'file_size': file_size,
                'synthesis_time': round(synthesis_time, 2),
                'text_length': len(test_text),
                'language': lang_key,
                'output_file': output_file
            }
            
            print(f"✅ {voice_name}: {file_size:,} bytes in {synthesis_time:.2f}s")
            return result
            
        else:
            result = {
                'voice': voice_name,
                'status': 'FAILED',
                'error': f"HTTP {response.status_code}: {response.text[:100]}",
                'synthesis_time': synthesis_time,
                'language': lang_key
            }
            print(f"❌ {voice_name}: HTTP {response.status_code}")
            return result
            
    except requests.exceptions.RequestException as e:
        result = {
            'voice': voice_name,
            'status': 'ERROR',
            'error': str(e)[:100],
            'language': lang_key
        }
        print(f"💥 {voice_name}: {str(e)[:50]}...")
        return result

def run_comprehensive_tests(voices, max_workers=3):
    """Run tests on all voices with controlled concurrency"""
    print(f"\n🚀 Starting Comprehensive Voice Tests ({len(voices)} voices)")
    print("=" * 70)
    
    results = []
    successful_tests = 0
    
    # Test voices in batches to avoid overwhelming the service
    for i, voice in enumerate(voices, 1):
        result = test_single_voice(voice, i, len(voices))
        results.append(result)
        
        if result['status'] == 'SUCCESS':
            successful_tests += 1
        
        # Small delay between tests to be gentle on the service
        time.sleep(0.5)
    
    return results, successful_tests

def generate_report(results, successful_tests, total_voices):
    """Generate comprehensive test report"""
    print("\n" + "=" * 70)
    print("📊 COMPREHENSIVE TEST REPORT")
    print("=" * 70)
    
    print(f"\n🎯 Overall Results:")
    print(f"   ✅ Successful: {successful_tests}/{total_voices} voices ({successful_tests/total_voices*100:.1f}%)")
    print(f"   ❌ Failed: {total_voices - successful_tests}/{total_voices} voices")
    
    # Group results by language
    lang_stats = {}
    for result in results:
        lang = result['language']
        if lang not in lang_stats:
            lang_stats[lang] = {'success': 0, 'failed': 0, 'total': 0}
        
        lang_stats[lang]['total'] += 1
        if result['status'] == 'SUCCESS':
            lang_stats[lang]['success'] += 1
        else:
            lang_stats[lang]['failed'] += 1
    
    print(f"\n🌍 Results by Language:")
    for lang, stats in sorted(lang_stats.items()):
        success_rate = stats['success'] / stats['total'] * 100
        status = "✅" if success_rate == 100 else "⚠️" if success_rate >= 50 else "❌"
        print(f"   {status} {lang.title()}: {stats['success']}/{stats['total']} ({success_rate:.0f}%)")
    
    # Performance statistics
    successful_results = [r for r in results if r['status'] == 'SUCCESS']
    if successful_results:
        avg_time = sum(r['synthesis_time'] for r in successful_results) / len(successful_results)
        avg_size = sum(r['file_size'] for r in successful_results) / len(successful_results)
        
        print(f"\n⚡ Performance Statistics:")
        print(f"   🕐 Average synthesis time: {avg_time:.2f}s")
        print(f"   📦 Average file size: {avg_size:,.0f} bytes")
    
    # Failed voices
    failed_results = [r for r in results if r['status'] != 'SUCCESS']
    if failed_results:
        print(f"\n❌ Failed Voices ({len(failed_results)}):")
        for result in failed_results:
            print(f"   • {result['voice']}: {result.get('error', 'Unknown error')}")
    
    # Save detailed results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"test_report_{timestamp}.json"
    
    report_data = {
        'timestamp': timestamp,
        'summary': {
            'total_voices': total_voices,
            'successful': successful_tests,
            'failed': total_voices - successful_tests,
            'success_rate': successful_tests / total_voices * 100
        },
        'language_stats': lang_stats,
        'detailed_results': results
    }
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Detailed report saved to: {report_file}")
    
    if Path("test_output").exists():
        wav_files = list(Path("test_output").glob("*.wav"))
        if wav_files:
            total_size = sum(f.stat().st_size for f in wav_files)
            print(f"📁 Generated {len(wav_files)} audio files ({total_size:,} bytes total)")

def main():
    """Main test execution"""
    print("🎉 Binary Piper TTS - Comprehensive Voice Test Suite")
    print("=" * 70)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 1: Check service health
    if not test_service_health():
        print("\n💥 Cannot proceed - TTS service is not available!")
        print("Please ensure the service is running on http://localhost:8000")
        return False
    
    # Step 2: Get available voices
    voices = get_available_voices()
    if not voices:
        print("\n💥 No voices available - cannot proceed with tests!")
        return False
    
    print(f"\n🎯 Will test all {len(voices)} voices with appropriate text for each language")
    
    # Step 3: Run comprehensive tests
    results, successful_tests = run_comprehensive_tests(voices)
    
    # Step 4: Generate report
    generate_report(results, successful_tests, len(voices))
    
    print(f"\n🏁 Testing completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return successful_tests == len(voices)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
