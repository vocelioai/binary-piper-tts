#!/usr/bin/env python3
"""
Binary Piper TTS - Advanced AI Features Demo
Comprehensive demonstration of voice cloning, audio effects, and SSML processing
"""

import os
import asyncio
import json
import tempfile
from pathlib import Path
import logging
from datetime import datetime

# Import our advanced modules
from advanced_features import AdvancedTTSEngine, SynthesisRequest
from audio_effects import EffectConfig, EffectType
from voice_cloning import VoiceCloningManager
from enhanced_ssml import SSMLProcessor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AdvancedTTSDemo:
    """Complete demonstration of advanced TTS features"""
    
    def __init__(self):
        self.engine = AdvancedTTSEngine()
        self.demo_outputs = Path("demo_outputs")
        self.demo_outputs.mkdir(exist_ok=True)
        
        print("🚀 BINARY PIPER TTS - ADVANCED AI FEATURES DEMO")
        print("=" * 80)
        print()
    
    async def run_complete_demo(self):
        """Run the complete advanced features demonstration"""
        
        # 1. Voice Cloning Demo
        await self.demo_voice_cloning()
        
        # 2. Audio Effects Demo  
        await self.demo_audio_effects()
        
        # 3. SSML Processing Demo
        await self.demo_ssml_processing()
        
        # 4. Advanced Integration Demo
        await self.demo_advanced_integration()
        
        # 5. Performance Analytics
        await self.demo_performance_analytics()
        
        print("\n" + "=" * 80)
        print("🎉 ADVANCED AI FEATURES DEMONSTRATION COMPLETE!")
        print("=" * 80)
    
    async def demo_voice_cloning(self):
        """Demonstrate voice cloning capabilities"""
        print("🧬 VOICE CLONING DEMONSTRATION")
        print("-" * 50)
        
        # Show available voice profiles
        profiles = self.engine.get_voice_profiles()
        print(f"📊 Available voice profiles: {len(profiles)}")
        
        if profiles:
            for profile in profiles[:3]:  # Show first 3
                print(f"   • {profile['name']} ({profile['language']}) - Quality: {profile['quality_score']:.3f}")
        
        # Create a demo voice profile (simulation)
        print("\n🎙️  Creating demo voice profile...")
        try:
            # In a real scenario, you would have actual audio files
            demo_audio_files = [
                str(self.demo_outputs / "demo_sample1.wav"),
                str(self.demo_outputs / "demo_sample2.wav")
            ]
            
            # Create placeholder audio files for demo
            self._create_demo_audio_files(demo_audio_files)
            
            profile_id = self.engine.create_voice_profile(
                audio_files=demo_audio_files,
                name="Demo Voice",
                language="en",
                gender="neutral",
                age_range="adult"
            )
            
            print(f"✅ Created voice profile: {profile_id}")
            
            # Test voice cloning synthesis
            cloning_request = SynthesisRequest(
                text="Hello! This is a demonstration of voice cloning technology.",
                voice_profile_id=profile_id,
                output_path=str(self.demo_outputs / "cloned_voice_demo.wav"),
                style_strength=1.0
            )
            
            result = await self.engine.synthesize_advanced(cloning_request)
            
            if result.success:
                print(f"🎵 Voice cloning synthesis: {result.output_path}")
                print(f"⏱️  Processing time: {result.processing_time:.2f}s")
                print(f"🎭 Voice used: {result.voice_used}")
            else:
                print(f"❌ Voice cloning failed: {result.error_message}")
        
        except Exception as e:
            print(f"💥 Voice cloning demo error: {e}")
        
        print()
    
    async def demo_audio_effects(self):
        """Demonstrate audio effects capabilities"""
        print("🎛️  AUDIO EFFECTS DEMONSTRATION")
        print("-" * 50)
        
        # Show available presets
        presets = self.engine.get_effects_presets()
        print(f"🎨 Available effects presets: {', '.join(presets)}")
        
        # Demo different effect presets
        effects_demos = [
            ("radio", "Professional radio announcer voice"),
            ("cathedral", "Spacious cathedral reverb"),
            ("robot", "Futuristic robotic voice"),
            ("dramatic", "Cinematic dramatic enhancement"),
            ("telephone", "Vintage telephone quality")
        ]
        
        for preset, description in effects_demos:
            print(f"\n🎭 {preset.upper()} PRESET: {description}")
            
            effects_request = SynthesisRequest(
                text=f"This is a demonstration of the {preset} audio effect preset.",
                voice_id="en-US-lessac-medium",
                effects_preset=preset,
                output_path=str(self.demo_outputs / f"effects_{preset}_demo.wav")
            )
            
            result = await self.engine.synthesize_advanced(effects_request)
            
            if result.success:
                print(f"   ✅ Generated: {result.output_path}")
                print(f"   🎨 Effects: {result.effects_applied}")
            else:
                print(f"   ❌ Failed: {result.error_message}")
        
        # Demo custom effects
        print(f"\n🔧 CUSTOM EFFECTS DEMO:")
        
        custom_effects_request = SynthesisRequest(
            text="This demonstrates custom audio effects configuration.",
            voice_id="en-US-ryan-high",
            custom_effects=[
                EffectConfig(EffectType.REVERB, {"room_size": 0.8, "wet_level": 0.5}, order=1),
                EffectConfig(EffectType.COMPRESSOR, {"threshold": 0.3, "ratio": 4.0}, order=2),
                EffectConfig(EffectType.EQUALIZER, {"low_gain": 1.2, "mid_gain": 1.0, "high_gain": 0.8}, order=3)
            ],
            output_path=str(self.demo_outputs / "custom_effects_demo.wav")
        )
        
        result = await self.engine.synthesize_advanced(custom_effects_request)
        
        if result.success:
            print(f"   ✅ Custom effects applied: {result.output_path}")
            print(f"   🎛️  Effects chain: {result.effects_applied}")
        else:
            print(f"   ❌ Custom effects failed: {result.error_message}")
        
        print()
    
    async def demo_ssml_processing(self):
        """Demonstrate SSML processing capabilities"""
        print("📝 SSML PROCESSING DEMONSTRATION")
        print("-" * 50)
        
        # Demo SSML examples
        ssml_demos = [
            {
                "name": "Prosody Control",
                "ssml": """<speak>
                    <prosody rate="slow" pitch="low">This is slow and low pitched.</prosody>
                    <break time="500ms"/>
                    <prosody rate="fast" pitch="high" volume="loud">This is fast, high, and loud!</prosody>
                </speak>"""
            },
            {
                "name": "Emphasis & Breaks",
                "ssml": """<speak>
                    Here's a sentence with a pause <break time="1s"/> and then some 
                    <emphasis level="strong">strong emphasis</emphasis>.
                    <break strength="weak"/>
                    <emphasis level="moderate">Moderate emphasis</emphasis> follows.
                </speak>"""
            },
            {
                "name": "Say-As Processing", 
                "ssml": """<speak>
                    Today is <say-as interpret-as="date">2024-01-15</say-as>.
                    The number is <say-as interpret-as="cardinal">12345</say-as>.
                    Call <say-as interpret-as="telephone">555-123-4567</say-as>.
                    <say-as interpret-as="spell-out">SSML</say-as> is powerful!
                </speak>"""
            },
            {
                "name": "Voice & Substitution",
                "ssml": """<speak>
                    <voice name="en-US-AriaNeural">
                        This is a different voice speaking.
                        <sub alias="World Wide Web">WWW</sub> is amazing!
                        <phoneme alphabet="ipa" ph="həˈloʊ">hello</phoneme> there!
                    </voice>
                </speak>"""
            },
            {
                "name": "Complex Structure",
                "ssml": """<speak xml:lang="en-US">
                    <p>
                        <s>This is the first sentence of the paragraph.</s>
                        <s>
                            <mark name="checkpoint1"/>
                            This sentence has a marker and 
                            <prosody pitch="+50%" rate="0.8">modified prosody</prosody>.
                        </s>
                    </p>
                    <break strength="strong"/>
                    <emphasis level="moderate">Thank you for listening to this demo!</emphasis>
                </speak>"""
            }
        ]
        
        for demo in ssml_demos:
            print(f"\n📄 {demo['name'].upper()}:")
            
            ssml_request = SynthesisRequest(
                text=demo['ssml'],
                voice_id="en-GB-alba-medium",
                ssml_enabled=True,
                effects_preset="dramatic",
                output_path=str(self.demo_outputs / f"ssml_{demo['name'].lower().replace(' ', '_')}_demo.wav")
            )
            
            result = await self.engine.synthesize_advanced(ssml_request)
            
            if result.success:
                print(f"   ✅ Generated: {result.output_path}")
                print(f"   📝 SSML segments: {result.ssml_segments}")
                print(f"   🎭 Voice: {result.voice_used}")
            else:
                print(f"   ❌ Failed: {result.error_message}")
        
        print()
    
    async def demo_advanced_integration(self):
        """Demonstrate advanced feature integration"""
        print("🚀 ADVANCED INTEGRATION DEMONSTRATION")
        print("-" * 50)
        
        # Complex integration demo
        integration_demos = [
            {
                "name": "Voice Cloning + SSML + Effects",
                "description": "Combines all three advanced features",
                "request": SynthesisRequest(
                    text="""<speak>
                        <prosody rate="0.9" pitch="+2st">
                            Hello! This demonstrates the complete integration of
                            <emphasis level="strong">voice cloning</emphasis>,
                            <break time="300ms"/>
                            <prosody volume="+3dB">audio effects</prosody>,
                            and <emphasis level="moderate">SSML processing</emphasis>.
                        </prosody>
                    </speak>""",
                    # voice_profile_id would be set if we had a real profile
                    voice_id="en-US-lessac-high",
                    effects_preset="radio",
                    ssml_enabled=True,
                    output_path=str(self.demo_outputs / "integration_full_demo.wav")
                )
            },
            {
                "name": "Multi-language SSML + Effects",
                "description": "SSML with effects for different languages",
                "request": SynthesisRequest(
                    text="""<speak>
                        <lang xml:lang="en-US">Hello in English.</lang>
                        <break time="500ms"/>
                        <lang xml:lang="de-DE">Hallo auf Deutsch.</lang>
                        <break time="500ms"/>
                        <lang xml:lang="es-ES">Hola en Español.</lang>
                    </speak>""",
                    voice_id="de-DE-thorsten-medium",
                    effects_preset="cathedral",
                    ssml_enabled=True,
                    output_path=str(self.demo_outputs / "integration_multilang_demo.wav")
                )
            },
            {
                "name": "Custom Effects + Complex SSML",
                "description": "Custom effects chain with advanced SSML",
                "request": SynthesisRequest(
                    text="""<speak>
                        <p>
                            <s>
                                <prosody rate="slow">
                                    This is a <emphasis level="strong">complex demonstration</emphasis>
                                    of <mark name="feature_highlight"/>advanced TTS capabilities.
                                </prosody>
                            </s>
                            <s>
                                <break time="800ms"/>
                                The processing includes <say-as interpret-as="cardinal">3</say-as>
                                major components working together seamlessly.
                            </s>
                        </p>
                    </speak>""",
                    voice_id="fr-FR-tom-medium",
                    custom_effects=[
                        EffectConfig(EffectType.COMPRESSOR, {"threshold": 0.4, "ratio": 3.0}, order=1),
                        EffectConfig(EffectType.REVERB, {"room_size": 0.6, "wet_level": 0.3}, order=2),
                        EffectConfig(EffectType.EQUALIZER, {"low_gain": 1.1, "mid_gain": 1.2, "high_gain": 0.9}, order=3)
                    ],
                    ssml_enabled=True,
                    output_path=str(self.demo_outputs / "integration_complex_demo.wav")
                )
            }
        ]
        
        for demo in integration_demos:
            print(f"\n🔥 {demo['name'].upper()}:")
            print(f"   📝 {demo['description']}")
            
            result = await self.engine.synthesize_advanced(demo['request'])
            
            if result.success:
                print(f"   ✅ Generated: {result.output_path}")
                print(f"   ⏱️  Processing: {result.processing_time:.2f}s")
                print(f"   🎵 Duration: {result.duration:.2f}s")
                print(f"   🎭 Voice: {result.voice_used}")
                print(f"   🎨 Effects: {result.effects_applied}")
                print(f"   📝 SSML segments: {result.ssml_segments}")
            else:
                print(f"   ❌ Failed: {result.error_message}")
        
        print()
    
    async def demo_performance_analytics(self):
        """Demonstrate performance analytics"""
        print("📊 PERFORMANCE ANALYTICS DEMONSTRATION")
        print("-" * 50)
        
        # Get comprehensive statistics
        stats = self.engine.get_processing_stats()
        
        print("🔢 SYNTHESIS STATISTICS:")
        print(f"   Total syntheses: {stats['total_syntheses']}")
        print(f"   Successful syntheses: {stats['successful_syntheses']}")
        print(f"   Success rate: {stats['success_rate']:.1%}")
        print(f"   Average processing time: {stats['average_processing_time']:.2f}s")
        print(f"   Total audio duration: {stats['total_audio_duration']:.1f}s")
        print(f"   Voice cloning usage: {stats['cloning_usage']} sessions")
        
        if stats['effects_usage']:
            print("\n🎨 EFFECTS USAGE:")
            for effect, count in sorted(stats['effects_usage'].items(), key=lambda x: x[1], reverse=True):
                print(f"   {effect}: {count} times")
        
        if stats['voice_usage']:
            print("\n🎭 VOICE USAGE:")
            for voice, count in sorted(stats['voice_usage'].items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"   {voice}: {count} times")
        
        # System capabilities summary
        print("\n🚀 SYSTEM CAPABILITIES:")
        print(f"   Available voices: {len(self.engine.get_available_voices())}")
        print(f"   Voice profiles: {len(self.engine.get_voice_profiles())}")
        print(f"   Effects presets: {len(self.engine.get_effects_presets())}")
        
        # Performance metrics
        if stats['total_syntheses'] > 0:
            efficiency = stats['total_audio_duration'] / (stats['average_processing_time'] * stats['successful_syntheses']) if stats['successful_syntheses'] > 0 else 0
            print(f"   Processing efficiency: {efficiency:.1f}x real-time")
        
        print()
    
    def _create_demo_audio_files(self, file_paths):
        """Create demo audio files for voice cloning demo"""
        import wave
        import struct
        import math
        
        for i, file_path in enumerate(file_paths):
            sample_rate = 16000
            duration = 3.0  # 3 seconds
            num_samples = int(sample_rate * duration)
            
            # Generate different tones for each file
            frequency = 440.0 + (i * 110.0)  # Different frequencies
            audio_data = []
            
            for j in range(num_samples):
                t = j / sample_rate
                # Simple sine wave with envelope
                envelope = math.exp(-t * 0.5)  # Decay envelope
                sample = envelope * 0.1 * math.sin(2 * math.pi * frequency * t)
                audio_data.append(struct.pack('<h', int(sample * 32767)))
            
            # Write WAV file
            with wave.open(file_path, 'wb') as wav_file:
                wav_file.setnchannels(1)  # mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(b''.join(audio_data))
        
        print(f"📁 Created {len(file_paths)} demo audio files")

def main():
    """Run the advanced TTS features demonstration"""
    
    try:
        # Create demo instance
        demo = AdvancedTTSDemo()
        
        # Run complete demonstration
        asyncio.run(demo.run_complete_demo())
        
        print(f"📁 Demo outputs saved to: {demo.demo_outputs}")
        print("🎧 Check the generated audio files to hear the results!")
        
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted by user")
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        print(f"💥 Demo error: {e}")

if __name__ == "__main__":
    main()
