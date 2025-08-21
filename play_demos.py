#!/usr/bin/env python3
"""
Binary Piper TTS - Interactive Demo Player
Play and explore the generated demo audio files
"""

import os
import subprocess
import sys
from pathlib import Path
import json
import time
from typing import Dict, List, Optional

class InteractiveDemoPlayer:
    """Interactive player for demo audio files"""
    
    def __init__(self, demo_dir: str = "demo_outputs"):
        self.demo_dir = Path(demo_dir)
        self.demo_files = {
            "🧬 Voice Cloning Demos": {
                "cloned_voice_demo.wav": "Voice cloning synthesis using custom profile",
                "demo_sample1.wav": "Reference audio sample 1 for voice training",
                "demo_sample2.wav": "Reference audio sample 2 for voice training"
            },
            "🎛️ Audio Effects Demos": {
                "effects_radio_demo.wav": "📻 Professional radio announcer voice",
                "effects_cathedral_demo.wav": "🏰 Spacious cathedral reverb",
                "effects_robot_demo.wav": "🤖 Futuristic robotic voice",
                "effects_dramatic_demo.wav": "🎭 Cinematic dramatic enhancement",
                "effects_telephone_demo.wav": "☎️ Vintage telephone quality",
                "custom_effects_demo.wav": "🔧 Custom effects chain (Reverb + Compressor + EQ)"
            },
            "📝 SSML Processing Demos": {
                "ssml_prosody_control_demo.wav": "Rate, pitch, and volume control",
                "ssml_emphasis_&_breaks_demo.wav": "Emphasis and timing control",
                "ssml_say-as_processing_demo.wav": "Number, date, and phone interpretation",
                "ssml_voice_&_substitution_demo.wav": "Voice switching and text substitution",
                "ssml_complex_structure_demo.wav": "Complex SSML structure with markers"
            },
            "🚀 Advanced Integration Demos": {
                "integration_full_demo.wav": "All features combined (SSML + Effects)",
                "integration_multilang_demo.wav": "Multi-language with cathedral effects",
                "integration_complex_demo.wav": "Complex SSML with custom effects chain"
            }
        }
        
        # Load analysis results if available
        self.analysis_data = self._load_analysis_report()
    
    def _load_analysis_report(self) -> Optional[Dict]:
        """Load audio analysis report if available"""
        report_path = self.demo_dir / "audio_analysis_report.json"
        if report_path.exists():
            try:
                with open(report_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load analysis report: {e}")
        return None
    
    def _get_file_info(self, filename: str) -> Dict:
        """Get file information from analysis data"""
        if not self.analysis_data:
            file_path = self.demo_dir / filename
            if file_path.exists():
                file_size = os.path.getsize(file_path)
                return {
                    "file_size_kb": round(file_size / 1024, 1),
                    "duration_seconds": "Unknown",
                    "sample_rate": "Unknown"
                }
            return {}
        
        # Find file in detailed results
        for result in self.analysis_data.get("detailed_results", []):
            if result["file_name"] == filename and result.get("is_valid"):
                return result
        
        return {}
    
    def _play_audio_windows(self, file_path: str) -> bool:
        """Play audio on Windows using built-in methods"""
        try:
            # Try to use Windows Media Player
            subprocess.run(["start", "", file_path], shell=True, check=True)
            return True
        except:
            try:
                # Try PowerShell with SoundPlayer
                ps_command = f'''
Add-Type -AssemblyName System.Windows.Forms
$player = New-Object System.Media.SoundPlayer "{file_path}"
$player.PlaySync()
'''
                subprocess.run(["powershell", "-Command", ps_command], check=True)
                return True
            except:
                return False
    
    def _play_audio_cross_platform(self, file_path: str) -> bool:
        """Cross-platform audio playback"""
        try:
            if sys.platform == "win32":
                return self._play_audio_windows(file_path)
            elif sys.platform == "darwin":  # macOS
                subprocess.run(["afplay", file_path], check=True)
                return True
            else:  # Linux
                # Try common Linux audio players
                for player in ["aplay", "paplay", "sox"]:
                    try:
                        subprocess.run([player, file_path], check=True)
                        return True
                    except:
                        continue
                return False
        except Exception as e:
            print(f"Error playing audio: {e}")
            return False
    
    def play_file(self, filename: str) -> bool:
        """Play a specific audio file"""
        file_path = self.demo_dir / filename
        if not file_path.exists():
            print(f"❌ File not found: {filename}")
            return False
        
        print(f"🎵 Playing: {filename}")
        
        # Get file info
        info = self._get_file_info(filename)
        if info:
            duration = info.get("duration_seconds", "Unknown")
            size = info.get("file_size_kb", "Unknown")
            sample_rate = info.get("sample_rate", "Unknown")
            print(f"   Duration: {duration}s | Size: {size}KB | Sample Rate: {sample_rate}Hz")
        
        success = self._play_audio_cross_platform(str(file_path))
        
        if not success:
            print(f"⚠️ Could not play audio automatically.")
            print(f"📁 Please manually open: {file_path}")
            print("   You can use Windows Media Player, VLC, or any audio player")
        
        return success
    
    def show_menu(self):
        """Show interactive menu"""
        while True:
            print("\n" + "=" * 70)
            print("🎧 BINARY PIPER TTS - INTERACTIVE DEMO PLAYER")
            print("=" * 70)
            
            if self.analysis_data:
                summary = self.analysis_data["summary"]
                print(f"📊 Analysis Summary: {summary['valid_files']} files | "
                      f"{summary['total_duration_seconds']:.1f}s total | "
                      f"{summary['total_size_kb']:.1f}KB")
                print()
            
            # Show categories
            category_num = 1
            category_map = {}
            file_map = {}
            file_num = 1
            
            for category, files in self.demo_files.items():
                print(f"{category_num}. {category}")
                category_map[str(category_num)] = category
                category_num += 1
                
                for filename, description in files.items():
                    file_path = self.demo_dir / filename
                    status = "✅" if file_path.exists() else "❌"
                    
                    info = self._get_file_info(filename)
                    duration_info = f" ({info.get('duration_seconds', '?')}s)" if info else ""
                    
                    print(f"   {file_num}. {status} {filename}{duration_info}")
                    print(f"      {description}")
                    file_map[str(file_num)] = filename
                    file_num += 1
                print()
            
            # Menu options
            print("Options:")
            print("   p [number] - Play specific file by number")
            print("   c [number] - Play all files in category")
            print("   a - Play all demo files")
            print("   s - Show statistics")
            print("   r - Refresh file list")
            print("   q - Quit")
            print()
            
            try:
                choice = input("Enter your choice: ").strip().lower()
                
                if choice == 'q':
                    print("👋 Goodbye!")
                    break
                
                elif choice == 'a':
                    self._play_all_files()
                
                elif choice == 's':
                    self._show_statistics()
                
                elif choice == 'r':
                    self.analysis_data = self._load_analysis_report()
                    print("🔄 File list refreshed!")
                
                elif choice.startswith('p '):
                    try:
                        file_num = choice.split()[1]
                        if file_num in file_map:
                            filename = file_map[file_num]
                            self.play_file(filename)
                        else:
                            print("❌ Invalid file number")
                    except:
                        print("❌ Invalid command format. Use: p [number]")
                
                elif choice.startswith('c '):
                    try:
                        cat_num = choice.split()[1]
                        if cat_num in category_map:
                            self._play_category(category_map[cat_num])
                        else:
                            print("❌ Invalid category number")
                    except:
                        print("❌ Invalid command format. Use: c [number]")
                
                else:
                    print("❌ Invalid choice. Please try again.")
            
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except EOFError:
                break
    
    def _play_category(self, category: str):
        """Play all files in a category"""
        print(f"\n🎵 Playing category: {category}")
        files = self.demo_files[category]
        
        for i, (filename, description) in enumerate(files.items(), 1):
            print(f"\n[{i}/{len(files)}] {description}")
            self.play_file(filename)
            
            if i < len(files):
                try:
                    input("Press Enter to continue to next file (or Ctrl+C to stop)...")
                except KeyboardInterrupt:
                    print("\n⏹️ Category playback stopped.")
                    break
    
    def _play_all_files(self):
        """Play all demo files"""
        print("\n🎵 Playing all demo files...")
        
        total_files = sum(len(files) for files in self.demo_files.values())
        current = 0
        
        for category, files in self.demo_files.items():
            print(f"\n📂 {category}")
            
            for filename, description in files.items():
                current += 1
                print(f"\n[{current}/{total_files}] {description}")
                self.play_file(filename)
                
                if current < total_files:
                    try:
                        input("Press Enter to continue (or Ctrl+C to stop)...")
                    except KeyboardInterrupt:
                        print("\n⏹️ Playback stopped.")
                        return
    
    def _show_statistics(self):
        """Show detailed statistics"""
        print("\n📊 DEMO AUDIO STATISTICS")
        print("-" * 50)
        
        if not self.analysis_data:
            print("❌ No analysis data available. Run test_demo_audio.py first.")
            return
        
        summary = self.analysis_data["summary"]
        print(f"Total Files: {summary['total_files']}")
        print(f"Valid Files: {summary['valid_files']}")
        print(f"Success Rate: {summary['success_rate']}")
        print(f"Total Duration: {summary['total_duration_seconds']:.1f} seconds")
        print(f"Total Size: {summary['total_size_kb']:.1f} KB ({summary['total_size_kb']/1024:.2f} MB)")
        
        print("\n📋 By Category:")
        for category, data in self.analysis_data["categories"].items():
            print(f"   {category.replace('_', ' ').title()}: "
                  f"{data['valid_count']}/{data['files_count']} files | "
                  f"{data['total_duration']:.1f}s")
        
        print("\n🎯 Quality Metrics:")
        detailed_results = self.analysis_data["detailed_results"]
        valid_files = [r for r in detailed_results if r.get("is_valid")]
        
        if valid_files:
            durations = [r["duration_seconds"] for r in valid_files]
            sizes = [r["file_size_kb"] for r in valid_files]
            sample_rates = [r["sample_rate"] for r in valid_files]
            
            print(f"   Duration range: {min(durations):.1f}s - {max(durations):.1f}s")
            print(f"   Size range: {min(sizes):.1f}KB - {max(sizes):.1f}KB")
            print(f"   Sample rates: {sorted(set(sample_rates))} Hz")
            
            # Peak levels
            peak_levels = [r.get("peak_db") for r in valid_files if r.get("peak_db") is not None]
            if peak_levels:
                print(f"   Peak level range: {min(peak_levels):.1f}dB - {max(peak_levels):.1f}dB")

def main():
    """Run interactive demo player"""
    player = InteractiveDemoPlayer()
    
    if not player.demo_dir.exists():
        print(f"❌ Demo directory not found: {player.demo_dir}")
        print("Please run advanced_demo.py first to generate the demo files.")
        return
    
    # Check for audio files
    wav_files = list(player.demo_dir.glob("*.wav"))
    if not wav_files:
        print(f"❌ No audio files found in {player.demo_dir}")
        print("Please run advanced_demo.py first to generate the demo files.")
        return
    
    print(f"🎧 Found {len(wav_files)} demo audio files!")
    print("Note: Audio playback requires system audio support.")
    print("If automatic playback fails, file paths will be provided for manual opening.")
    
    try:
        player.show_menu()
    except Exception as e:
        print(f"💥 Player error: {e}")

if __name__ == "__main__":
    main()
