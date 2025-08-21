#!/usr/bin/env python3
"""
Binary Piper TTS - Demo Audio File Analyzer
Comprehensive analysis of generated demo audio files
"""

import os
import wave
import json
from pathlib import Path
from typing import Dict, List, Any, Tuple
import logging
from datetime import datetime
import struct
import math

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AudioAnalyzer:
    """Analyze audio file properties and quality"""
    
    def __init__(self):
        self.analysis_results = []
        
    def analyze_wav_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a WAV audio file"""
        try:
            with wave.open(file_path, 'rb') as wav_file:
                # Basic properties
                frames = wav_file.getnframes()
                sample_rate = wav_file.getframerate()
                channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                duration = frames / sample_rate if sample_rate > 0 else 0
                
                # Read audio data for analysis
                audio_data = wav_file.readframes(frames)
                
                # Convert to numpy-like analysis
                if sample_width == 1:
                    samples = [struct.unpack('B', audio_data[i:i+1])[0] for i in range(0, len(audio_data), 1)]
                    samples = [(s - 128) / 128.0 for s in samples]
                elif sample_width == 2:
                    samples = [struct.unpack('<h', audio_data[i:i+2])[0] for i in range(0, len(audio_data), 2)]
                    samples = [s / 32768.0 for s in samples]
                else:
                    samples = []
                
                # Calculate audio statistics
                if samples:
                    max_amplitude = max(abs(s) for s in samples)
                    rms_level = math.sqrt(sum(s*s for s in samples) / len(samples))
                    peak_db = 20 * math.log10(max_amplitude) if max_amplitude > 0 else -float('inf')
                    rms_db = 20 * math.log10(rms_level) if rms_level > 0 else -float('inf')
                    
                    # Dynamic range analysis
                    non_zero_samples = [abs(s) for s in samples if abs(s) > 0.001]
                    if non_zero_samples:
                        dynamic_range = max(non_zero_samples) / min(non_zero_samples)
                        dynamic_range_db = 20 * math.log10(dynamic_range)
                    else:
                        dynamic_range_db = 0.0
                else:
                    max_amplitude = 0.0
                    rms_level = 0.0
                    peak_db = -float('inf')
                    rms_db = -float('inf')
                    dynamic_range_db = 0.0
                
                file_size = os.path.getsize(file_path)
                
                return {
                    "file_name": os.path.basename(file_path),
                    "file_size_bytes": file_size,
                    "file_size_kb": round(file_size / 1024, 2),
                    "duration_seconds": round(duration, 2),
                    "sample_rate": sample_rate,
                    "channels": channels,
                    "sample_width_bits": sample_width * 8,
                    "total_samples": frames,
                    "max_amplitude": round(max_amplitude, 4),
                    "rms_level": round(rms_level, 4),
                    "peak_db": round(peak_db, 2) if peak_db != -float('inf') else None,
                    "rms_db": round(rms_db, 2) if rms_db != -float('inf') else None,
                    "dynamic_range_db": round(dynamic_range_db, 2),
                    "bitrate_kbps": round((sample_rate * channels * sample_width * 8) / 1000, 1),
                    "is_valid": True,
                    "error": None
                }
                
        except Exception as e:
            logger.error(f"Failed to analyze {file_path}: {e}")
            return {
                "file_name": os.path.basename(file_path),
                "file_size_bytes": os.path.getsize(file_path) if os.path.exists(file_path) else 0,
                "is_valid": False,
                "error": str(e)
            }

class DemoAudioTester:
    """Test all demo audio files"""
    
    def __init__(self, demo_dir: str = "demo_outputs"):
        self.demo_dir = Path(demo_dir)
        self.analyzer = AudioAnalyzer()
        self.demo_categories = {
            "voice_cloning": [
                "cloned_voice_demo.wav",
                "demo_sample1.wav", 
                "demo_sample2.wav"
            ],
            "audio_effects": [
                "effects_radio_demo.wav",
                "effects_cathedral_demo.wav",
                "effects_robot_demo.wav",
                "effects_dramatic_demo.wav",
                "effects_telephone_demo.wav",
                "custom_effects_demo.wav"
            ],
            "ssml_processing": [
                "ssml_prosody_control_demo.wav",
                "ssml_emphasis_&_breaks_demo.wav",
                "ssml_say-as_processing_demo.wav",
                "ssml_voice_&_substitution_demo.wav",
                "ssml_complex_structure_demo.wav"
            ],
            "advanced_integration": [
                "integration_full_demo.wav",
                "integration_multilang_demo.wav",
                "integration_complex_demo.wav"
            ]
        }
        
    def test_all_demos(self) -> Dict[str, Any]:
        """Test all demo audio files"""
        print("🎧 BINARY PIPER TTS - DEMO AUDIO FILE TESTING")
        print("=" * 70)
        
        if not self.demo_dir.exists():
            print(f"❌ Demo directory not found: {self.demo_dir}")
            return {"success": False, "error": "Demo directory not found"}
        
        # Get all WAV files in demo directory
        wav_files = list(self.demo_dir.glob("*.wav"))
        print(f"📁 Found {len(wav_files)} audio files in {self.demo_dir}")
        print()
        
        if not wav_files:
            print("❌ No audio files found!")
            return {"success": False, "error": "No audio files found"}
        
        # Analyze all files
        all_results = []
        category_results = {}
        
        # Test by category
        for category, file_list in self.demo_categories.items():
            print(f"🔍 TESTING {category.upper().replace('_', ' ')}:")
            category_files = []
            
            for file_name in file_list:
                file_path = self.demo_dir / file_name
                if file_path.exists():
                    result = self.analyzer.analyze_wav_file(str(file_path))
                    all_results.append(result)
                    category_files.append(result)
                    
                    # Display result
                    if result["is_valid"]:
                        print(f"   ✅ {result['file_name']}")
                        print(f"      Duration: {result['duration_seconds']}s | "
                              f"Size: {result['file_size_kb']}KB | "
                              f"Sample Rate: {result['sample_rate']}Hz")
                        if result['peak_db'] is not None:
                            print(f"      Peak: {result['peak_db']}dB | "
                                  f"RMS: {result['rms_db']}dB | "
                                  f"Dynamic Range: {result['dynamic_range_db']}dB")
                    else:
                        print(f"   ❌ {result['file_name']} - ERROR: {result['error']}")
                else:
                    print(f"   ❌ {file_name} - FILE NOT FOUND")
                    all_results.append({
                        "file_name": file_name,
                        "is_valid": False,
                        "error": "File not found"
                    })
            
            category_results[category] = category_files
            print()
        
        # Overall statistics
        valid_files = [r for r in all_results if r["is_valid"]]
        invalid_files = [r for r in all_results if not r["is_valid"]]
        
        print("📊 OVERALL STATISTICS:")
        print(f"   Total files analyzed: {len(all_results)}")
        print(f"   Valid audio files: {len(valid_files)}")
        print(f"   Invalid/missing files: {len(invalid_files)}")
        print(f"   Success rate: {len(valid_files)/len(all_results)*100:.1f}%")
        
        if valid_files:
            total_duration = sum(r["duration_seconds"] for r in valid_files)
            total_size_kb = sum(r["file_size_kb"] for r in valid_files)
            avg_sample_rate = sum(r["sample_rate"] for r in valid_files) / len(valid_files)
            
            print(f"   Total audio duration: {total_duration:.1f} seconds")
            print(f"   Total file size: {total_size_kb:.1f} KB ({total_size_kb/1024:.2f} MB)")
            print(f"   Average sample rate: {avg_sample_rate:.0f} Hz")
            
            # Quality statistics
            peak_levels = [r["peak_db"] for r in valid_files if r["peak_db"] is not None]
            if peak_levels:
                print(f"   Peak level range: {min(peak_levels):.1f} to {max(peak_levels):.1f} dB")
        
        print()
        
        # Category breakdown
        print("📋 CATEGORY BREAKDOWN:")
        for category, results in category_results.items():
            valid_in_category = sum(1 for r in results if r["is_valid"])
            total_in_category = len(self.demo_categories[category])
            print(f"   {category.replace('_', ' ').title()}: {valid_in_category}/{total_in_category} files")
        
        print()
        
        # Audio quality assessment
        if valid_files:
            print("🎯 AUDIO QUALITY ASSESSMENT:")
            
            # Check for consistent audio properties
            sample_rates = set(r["sample_rate"] for r in valid_files)
            channels = set(r["channels"] for r in valid_files)
            bit_depths = set(r["sample_width_bits"] for r in valid_files)
            
            print(f"   Sample rates used: {sorted(sample_rates)} Hz")
            print(f"   Channel configurations: {sorted(channels)} ({'mono' if 1 in channels else 'stereo/multi'})")
            print(f"   Bit depths: {sorted(bit_depths)} bits")
            
            # Quality indicators
            good_quality_files = [r for r in valid_files if r.get("peak_db", -100) > -20 and r.get("dynamic_range_db", 0) > 20]
            print(f"   High quality files: {len(good_quality_files)}/{len(valid_files)}")
            
            # Duration analysis
            durations = [r["duration_seconds"] for r in valid_files]
            if durations:
                print(f"   Duration range: {min(durations):.1f}s to {max(durations):.1f}s")
                print(f"   Average duration: {sum(durations)/len(durations):.1f}s")
        
        # Missing files report
        if invalid_files:
            print("\n❌ ISSUES FOUND:")
            for result in invalid_files:
                print(f"   • {result['file_name']}: {result['error']}")
        
        # Success summary
        success = len(invalid_files) == 0
        
        print(f"\n{'🎉 ALL TESTS PASSED!' if success else '⚠️ SOME ISSUES FOUND'}")
        print("=" * 70)
        
        return {
            "success": success,
            "total_files": len(all_results),
            "valid_files": len(valid_files),
            "invalid_files": len(invalid_files),
            "success_rate": len(valid_files)/len(all_results)*100 if all_results else 0,
            "total_duration": sum(r["duration_seconds"] for r in valid_files),
            "total_size_kb": sum(r["file_size_kb"] for r in valid_files),
            "categories": category_results,
            "detailed_results": all_results
        }
    
    def create_audio_report(self, results: Dict[str, Any]) -> str:
        """Create detailed audio analysis report"""
        report_path = self.demo_dir / "audio_analysis_report.json"
        
        report_data = {
            "analysis_timestamp": datetime.now().isoformat(),
            "summary": {
                "total_files": results["total_files"],
                "valid_files": results["valid_files"],
                "success_rate": f"{results['success_rate']:.1f}%",
                "total_duration_seconds": results["total_duration"],
                "total_size_kb": results["total_size_kb"]
            },
            "categories": {
                category: {
                    "files_count": len(files),
                    "valid_count": sum(1 for f in files if f["is_valid"]),
                    "total_duration": sum(f.get("duration_seconds", 0) for f in files if f["is_valid"]),
                    "files": files
                }
                for category, files in results["categories"].items()
            },
            "detailed_results": results["detailed_results"]
        }
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Detailed report saved: {report_path}")
        return str(report_path)

def main():
    """Run demo audio testing"""
    tester = DemoAudioTester()
    
    try:
        # Test all demo files
        results = tester.test_all_demos()
        
        # Create detailed report
        tester.create_audio_report(results)
        
        # Final status
        if results["success"]:
            print("\n🎊 DEMO TESTING COMPLETE - ALL FILES VALID! 🎊")
        else:
            print(f"\n⚠️ DEMO TESTING COMPLETE - {results['invalid_files']} ISSUES FOUND")
        
        return results["success"]
        
    except Exception as e:
        logger.error(f"Demo testing failed: {e}")
        print(f"💥 Testing error: {e}")
        return False

if __name__ == "__main__":
    main()
