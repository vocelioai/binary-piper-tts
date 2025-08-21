#!/usr/bin/env python3
"""
Binary Piper TTS - Production Analytics Dashboard
Advanced monitoring and analytics for production deployment
"""

import requests
import json
import time
from datetime import datetime, timezone
from collections import defaultdict, Counter
import statistics

class ProductionAnalytics:
    def __init__(self, base_url="https://binary-piper-tts-production.up.railway.app"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.timeout = 30
        
    def get_system_health(self):
        """Get comprehensive system health metrics"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_voices_analytics(self):
        """Get detailed voice analytics"""
        try:
            # Get voices list
            voices_response = self.session.get(f"{self.base_url}/voices")
            voices_response.raise_for_status()
            voices = voices_response.json()
            
            # Get detailed voice info
            detailed_response = self.session.get(f"{self.base_url}/voices/detailed")
            detailed_response.raise_for_status()
            detailed = detailed_response.json()
            
            return self._analyze_voices(voices, detailed)
        except Exception as e:
            return {"error": str(e)}
    
    def _analyze_voices(self, voices, detailed_data):
        """Analyze voice data and generate insights"""
        if not voices:
            return {"total": 0, "error": "No voices available"}
        
        # Basic metrics
        total_voices = len(voices)
        
        # Language analysis
        languages = defaultdict(list)
        quality_levels = defaultdict(int)
        regions = defaultdict(int)
        
        for voice in voices:
            # Extract language/region (e.g., 'en_US', 'fr_FR')
            parts = voice.split('-')
            if len(parts) >= 2:
                lang_region = parts[0]
                quality = parts[-1] if parts[-1] in ['low', 'medium', 'high', 'x_low'] else 'medium'
                
                languages[lang_region.split('_')[0]].append(voice)
                quality_levels[quality] += 1
                regions[lang_region] += 1
        
        # Calculate diversity metrics
        language_diversity = len(languages)
        region_diversity = len(regions)
        quality_distribution = dict(quality_levels)
        
        # Top languages by voice count
        top_languages = dict(Counter({lang: len(voices_list) 
                                    for lang, voices_list in languages.items()}).most_common(10))
        
        return {
            "total_voices": total_voices,
            "language_diversity": language_diversity,
            "region_diversity": region_diversity,
            "quality_distribution": quality_distribution,
            "top_languages": top_languages,
            "languages_breakdown": dict(languages),
            "regions_breakdown": dict(regions),
            "detailed_info": detailed_data.get("voices", {}) if detailed_data else {}
        }
    
    def performance_benchmark(self, test_texts=None, sample_voices=5):
        """Run performance benchmarks"""
        if test_texts is None:
            test_texts = [
                "Hello world",
                "This is a performance test of the Binary Piper TTS service.",
                "The quick brown fox jumps over the lazy dog. This sentence contains every letter of the alphabet and is commonly used for testing purposes in typography and speech synthesis applications."
            ]
        
        # Get available voices
        try:
            voices_response = self.session.get(f"{self.base_url}/voices")
            voices = voices_response.json()
            
            if not voices:
                return {"error": "No voices available for testing"}
            
            # Sample voices for testing
            test_voices = voices[:sample_voices] if len(voices) > sample_voices else voices
            
            results = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "test_configuration": {
                    "voices_tested": len(test_voices),
                    "texts_tested": len(test_texts),
                    "total_requests": len(test_voices) * len(test_texts)
                },
                "performance_metrics": {},
                "voice_performance": {}
            }
            
            all_response_times = []
            
            print("🔥 Running Performance Benchmarks...")
            print(f"   Testing {len(test_voices)} voices with {len(test_texts)} text samples")
            
            for voice in test_voices:
                voice_times = []
                
                for text in test_texts:
                    start_time = time.time()
                    
                    try:
                        response = self.session.post(
                            f"{self.base_url}/synthesize",
                            json={"text": text, "voice": voice},
                            timeout=60
                        )
                        
                        end_time = time.time()
                        response_time = end_time - start_time
                        
                        if response.status_code == 200:
                            voice_times.append(response_time)
                            all_response_times.append(response_time)
                            print(f"   ✅ {voice}: {response_time:.2f}s")
                        else:
                            print(f"   ❌ {voice}: HTTP {response.status_code}")
                    
                    except Exception as e:
                        print(f"   ❌ {voice}: {str(e)[:50]}...")
                
                if voice_times:
                    results["voice_performance"][voice] = {
                        "avg_response_time": statistics.mean(voice_times),
                        "min_response_time": min(voice_times),
                        "max_response_time": max(voice_times),
                        "successful_requests": len(voice_times)
                    }
            
            # Overall performance metrics
            if all_response_times:
                results["performance_metrics"] = {
                    "avg_response_time": statistics.mean(all_response_times),
                    "median_response_time": statistics.median(all_response_times),
                    "min_response_time": min(all_response_times),
                    "max_response_time": max(all_response_times),
                    "p95_response_time": statistics.quantiles(all_response_times, n=20)[18] if len(all_response_times) > 10 else max(all_response_times),
                    "total_successful_requests": len(all_response_times),
                    "success_rate": len(all_response_times) / (len(test_voices) * len(test_texts)) * 100
                }
            
            return results
            
        except Exception as e:
            return {"error": f"Performance benchmark failed: {e}"}
    
    def generate_dashboard_report(self):
        """Generate comprehensive dashboard report"""
        print("🎯 BINARY PIPER TTS - PRODUCTION ANALYTICS DASHBOARD")
        print("=" * 80)
        print(f"📊 Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print()
        
        # System Health
        print("🔍 SYSTEM HEALTH")
        print("-" * 40)
        health = self.get_system_health()
        if health.get("status") == "healthy":
            print("✅ Status: HEALTHY")
            if "checks" in health:
                for check_name, check_data in health["checks"].items():
                    status_icon = "✅" if check_data.get("status") == "ok" else "❌"
                    print(f"   {status_icon} {check_name}: {check_data.get('message', 'OK')}")
        else:
            print("❌ Status: UNHEALTHY")
            print(f"   Error: {health.get('message', 'Unknown error')}")
        print()
        
        # Voice Analytics
        print("🎵 VOICE ANALYTICS")
        print("-" * 40)
        voice_analytics = self.get_voices_analytics()
        
        if "error" not in voice_analytics:
            print(f"📊 Total Voices: {voice_analytics['total_voices']}")
            print(f"🌍 Languages Supported: {voice_analytics['language_diversity']}")
            print(f"🗺️  Regions Covered: {voice_analytics['region_diversity']}")
            
            print("\n🏆 Top Languages:")
            for lang, count in list(voice_analytics['top_languages'].items())[:5]:
                percentage = (count / voice_analytics['total_voices']) * 100
                print(f"   {lang.upper()}: {count} voices ({percentage:.1f}%)")
            
            print("\n🎯 Quality Distribution:")
            for quality, count in voice_analytics['quality_distribution'].items():
                percentage = (count / voice_analytics['total_voices']) * 100
                print(f"   {quality.upper()}: {count} voices ({percentage:.1f}%)")
        else:
            print(f"❌ Voice Analytics Error: {voice_analytics['error']}")
        print()
        
        # Performance Metrics
        print("⚡ PERFORMANCE BENCHMARKS")
        print("-" * 40)
        perf_results = self.performance_benchmark()
        
        if "error" not in perf_results:
            metrics = perf_results.get("performance_metrics", {})
            config = perf_results.get("test_configuration", {})
            
            print(f"🧪 Test Configuration: {config.get('total_requests', 0)} total requests")
            print(f"   Voices: {config.get('voices_tested', 0)}")
            print(f"   Text Samples: {config.get('texts_tested', 0)}")
            
            if metrics:
                print(f"\n📈 Performance Results:")
                print(f"   ✅ Success Rate: {metrics.get('success_rate', 0):.1f}%")
                print(f"   ⚡ Average Response: {metrics.get('avg_response_time', 0):.2f}s")
                print(f"   🚀 Fastest Response: {metrics.get('min_response_time', 0):.2f}s")
                print(f"   🐌 Slowest Response: {metrics.get('max_response_time', 0):.2f}s")
                print(f"   📊 95th Percentile: {metrics.get('p95_response_time', 0):.2f}s")
                
                # Performance rating
                avg_time = metrics.get('avg_response_time', 0)
                if avg_time < 1.0:
                    rating = "🚀 EXCELLENT"
                elif avg_time < 2.0:
                    rating = "✅ GOOD"
                elif avg_time < 5.0:
                    rating = "⚠️  ACCEPTABLE"
                else:
                    rating = "❌ NEEDS IMPROVEMENT"
                
                print(f"   🎯 Overall Rating: {rating}")
        else:
            print(f"❌ Performance Test Error: {perf_results['error']}")
        
        print()
        print("=" * 80)
        print("🎉 Dashboard Report Complete!")
        
        return {
            "health": health,
            "voice_analytics": voice_analytics,
            "performance": perf_results
        }

def main():
    """Run production analytics dashboard"""
    analytics = ProductionAnalytics()
    dashboard_data = analytics.generate_dashboard_report()
    
    # Save detailed report to JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"production_analytics_{timestamp}.json"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(dashboard_data, f, indent=2, default=str)
    
    print(f"📁 Detailed report saved: {report_file}")

if __name__ == "__main__":
    main()
