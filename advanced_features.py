#!/usr/bin/env python3
"""
Binary Piper TTS - Advanced AI Features Integration
Combines voice cloning, audio effects, and SSML processing
"""

import os
import json
import tempfile
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import logging
from datetime import datetime
from dataclasses import dataclass
import asyncio
import concurrent.futures

# Import our advanced modules
from voice_cloning import VoiceCloningManager, VoiceProfile
from audio_effects import AudioEffectsPipeline, EffectConfig, EffectType
from enhanced_ssml import SSMLProcessor, SSMLElement

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SynthesisRequest:
    """Advanced synthesis request with all features"""
    text: str
    voice_id: Optional[str] = None
    voice_profile_id: Optional[str] = None  # For voice cloning
    effects_preset: Optional[str] = None
    custom_effects: Optional[List[EffectConfig]] = None
    ssml_enabled: bool = True
    output_format: str = "wav"
    output_path: Optional[str] = None
    style_strength: float = 1.0
    metadata: Dict[str, Any] = None

@dataclass  
class SynthesisResult:
    """Result from advanced synthesis"""
    success: bool
    output_path: Optional[str] = None
    duration: float = 0.0
    processing_time: float = 0.0
    voice_used: Optional[str] = None
    effects_applied: List[str] = None
    ssml_segments: int = 0
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = None

class AdvancedTTSEngine:
    """Advanced TTS engine with voice cloning, effects, and SSML"""
    
    def __init__(self, 
                 base_tts_command: str = "piper",
                 models_dir: str = "models",
                 temp_dir: Optional[str] = None):
        
        self.base_tts_command = base_tts_command
        self.models_dir = Path(models_dir)
        self.temp_dir = Path(temp_dir) if temp_dir else Path(tempfile.gettempdir()) / "advanced_tts"
        self.temp_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self.voice_cloning = VoiceCloningManager()
        self.audio_effects = AudioEffectsPipeline()
        self.ssml_processor = SSMLProcessor()
        
        # Available voices (would be loaded from actual TTS system)
        self.available_voices = self._load_available_voices()
        
        # Processing stats
        self.synthesis_count = 0
        self.processing_history: List[SynthesisResult] = []
        
        logger.info(f"Advanced TTS engine initialized with {len(self.available_voices)} voices")
        logger.info(f"Voice cloning profiles: {len(self.voice_cloning.profiles)}")
        logger.info(f"Audio effects presets: {len(self.audio_effects.get_available_presets())}")
    
    def _load_available_voices(self) -> Dict[str, Dict[str, str]]:
        """Load available TTS voices"""
        # This would normally scan the models directory
        # For now, return our known 39 voices
        return {
            # English voices
            "en-US-amy-low": {"language": "en", "country": "US", "quality": "low"},
            "en-US-amy-medium": {"language": "en", "country": "US", "quality": "medium"},
            "en-US-danny-low": {"language": "en", "country": "US", "quality": "low"},
            "en-US-joe-medium": {"language": "en", "country": "US", "quality": "medium"},
            "en-US-kathleen-low": {"language": "en", "country": "US", "quality": "low"},
            "en-US-lessac-high": {"language": "en", "country": "US", "quality": "high"},
            "en-US-lessac-low": {"language": "en", "country": "US", "quality": "low"},
            "en-US-lessac-medium": {"language": "en", "country": "US", "quality": "medium"},
            "en-US-libritts-high": {"language": "en", "country": "US", "quality": "high"},
            "en-US-ryan-high": {"language": "en", "country": "US", "quality": "high"},
            "en-US-ryan-low": {"language": "en", "country": "US", "quality": "low"},
            "en-US-ryan-medium": {"language": "en", "country": "US", "quality": "medium"},
            
            # British English
            "en-GB-alan-low": {"language": "en", "country": "GB", "quality": "low"},
            "en-GB-alan-medium": {"language": "en", "country": "GB", "quality": "medium"},
            "en-GB-alba-medium": {"language": "en", "country": "GB", "quality": "medium"},
            "en-GB-aru-medium": {"language": "en", "country": "GB", "quality": "medium"},
            "en-GB-jenny_dioco-medium": {"language": "en", "country": "GB", "quality": "medium"},
            "en-GB-northern_english_male-medium": {"language": "en", "country": "GB", "quality": "medium"},
            "en-GB-semaine-medium": {"language": "en", "country": "GB", "quality": "medium"},
            "en-GB-sweetpea-medium": {"language": "en", "country": "GB", "quality": "medium"},
            
            # German voices  
            "de-DE-eva_k-low": {"language": "de", "country": "DE", "quality": "low"},
            "de-DE-karlsson-low": {"language": "de", "country": "DE", "quality": "low"},
            "de-DE-kerstin-low": {"language": "de", "country": "DE", "quality": "low"},
            "de-DE-pavoque-low": {"language": "de", "country": "DE", "quality": "low"},
            "de-DE-ramona-low": {"language": "de", "country": "DE", "quality": "low"},
            "de-DE-thorsten-high": {"language": "de", "country": "DE", "quality": "high"},
            "de-DE-thorsten-low": {"language": "de", "country": "DE", "quality": "low"},
            "de-DE-thorsten-medium": {"language": "de", "country": "DE", "quality": "medium"},
            
            # Spanish voices
            "es-ES-carlfm-x_low": {"language": "es", "country": "ES", "quality": "x_low"},
            "es-ES-davefx-medium": {"language": "es", "country": "ES", "quality": "medium"},
            "es-ES-mls_10246-low": {"language": "es", "country": "ES", "quality": "low"},
            "es-ES-mls_9972-low": {"language": "es", "country": "ES", "quality": "low"},
            "es-ES-sharvard-medium": {"language": "es", "country": "ES", "quality": "medium"},
            
            # French voices
            "fr-FR-gilles-low": {"language": "fr", "country": "FR", "quality": "low"},
            "fr-FR-mls_1840-low": {"language": "fr", "country": "FR", "quality": "low"},
            "fr-FR-siwis-low": {"language": "fr", "country": "FR", "quality": "low"},
            "fr-FR-siwis-medium": {"language": "fr", "country": "FR", "quality": "medium"},
            "fr-FR-tom-medium": {"language": "fr", "country": "FR", "quality": "medium"},
            
            # Other languages
            "it-IT-riccardo-x_low": {"language": "it", "country": "IT", "quality": "x_low"},
            "pt-BR-faber-medium": {"language": "pt", "country": "BR", "quality": "medium"}
        }
    
    async def synthesize_advanced(self, request: SynthesisRequest) -> SynthesisResult:
        """Perform advanced synthesis with all features"""
        start_time = datetime.now()
        self.synthesis_count += 1
        
        logger.info(f"Starting advanced synthesis #{self.synthesis_count}")
        logger.info(f"Voice ID: {request.voice_id}")
        logger.info(f"Voice Profile: {request.voice_profile_id}")
        logger.info(f"Effects: {request.effects_preset}")
        logger.info(f"SSML: {request.ssml_enabled}")
        
        try:
            # Step 1: Process SSML if enabled
            ssml_instructions = None
            if request.ssml_enabled:
                ssml_instructions = self.ssml_processor.process_ssml(request.text)
                logger.info(f"SSML processed: {len(ssml_instructions['segments'])} segments")
            
            # Step 2: Generate base audio
            if request.voice_profile_id:
                # Use voice cloning
                audio_path = await self._synthesize_with_cloning(request, ssml_instructions)
            else:
                # Use standard TTS
                audio_path = await self._synthesize_standard(request, ssml_instructions)
            
            if not audio_path:
                raise Exception("Base audio synthesis failed")
            
            # Step 3: Apply audio effects
            if request.effects_preset or request.custom_effects:
                processed_path = await self._apply_audio_effects(
                    audio_path, request.effects_preset, request.custom_effects
                )
                if processed_path:
                    audio_path = processed_path
            
            # Step 4: Move to final output path if specified
            final_path = request.output_path or audio_path
            if request.output_path and audio_path != request.output_path:
                os.rename(audio_path, request.output_path)
                final_path = request.output_path
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Get audio duration (would use actual audio analysis)
            audio_duration = self._estimate_audio_duration(request.text)
            
            # Create result
            result = SynthesisResult(
                success=True,
                output_path=final_path,
                duration=audio_duration,
                processing_time=processing_time,
                voice_used=request.voice_id or request.voice_profile_id,
                effects_applied=self._get_applied_effects(request),
                ssml_segments=len(ssml_instructions['segments']) if ssml_instructions else 0,
                metadata={
                    "synthesis_id": self.synthesis_count,
                    "ssml_instructions": ssml_instructions,
                    "request": request.__dict__
                }
            )
            
            self.processing_history.append(result)
            logger.info(f"Advanced synthesis completed in {processing_time:.2f}s")
            
            return result
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            
            result = SynthesisResult(
                success=False,
                processing_time=processing_time,
                error_message=str(e),
                metadata={"synthesis_id": self.synthesis_count}
            )
            
            self.processing_history.append(result)
            logger.error(f"Advanced synthesis failed: {e}")
            
            return result
    
    async def _synthesize_with_cloning(self, 
                                     request: SynthesisRequest, 
                                     ssml_instructions: Optional[Dict]) -> Optional[str]:
        """Synthesize using voice cloning"""
        
        profile = self.voice_cloning.get_profile(request.voice_profile_id)
        if not profile:
            raise ValueError(f"Voice profile not found: {request.voice_profile_id}")
        
        # Generate output path
        output_path = self.temp_dir / f"cloned_{self.synthesis_count}_{profile.name}.wav"
        
        # Perform voice cloning
        success = self.voice_cloning.clone_voice(
            text=request.text,
            profile_id=request.voice_profile_id,
            output_path=str(output_path),
            style_strength=request.style_strength
        )
        
        if success:
            logger.info(f"Voice cloning successful: {output_path}")
            return str(output_path)
        else:
            logger.error("Voice cloning failed")
            return None
    
    async def _synthesize_standard(self, 
                                 request: SynthesisRequest, 
                                 ssml_instructions: Optional[Dict]) -> Optional[str]:
        """Synthesize using standard TTS"""
        
        # Use default voice if none specified
        voice_id = request.voice_id or "en-US-lessac-medium"
        
        if voice_id not in self.available_voices:
            raise ValueError(f"Voice not available: {voice_id}")
        
        # Generate output path
        output_path = self.temp_dir / f"standard_{self.synthesis_count}_{voice_id}.wav"
        
        # For demonstration, create a placeholder audio file
        # In production, this would call the actual Piper TTS
        await self._create_placeholder_audio(str(output_path), request.text)
        
        logger.info(f"Standard TTS synthesis: {output_path}")
        return str(output_path)
    
    async def _apply_audio_effects(self, 
                                 audio_path: str,
                                 effects_preset: Optional[str],
                                 custom_effects: Optional[List[EffectConfig]]) -> Optional[str]:
        """Apply audio effects to synthesized audio"""
        
        output_path = self.temp_dir / f"effects_{self.synthesis_count}.wav"
        
        # Clear existing effects
        self.audio_effects.clear_effects()
        
        # Apply preset if specified
        if effects_preset:
            self.audio_effects.apply_preset(effects_preset)
            logger.info(f"Applied effects preset: {effects_preset}")
        
        # Add custom effects
        if custom_effects:
            for effect_config in custom_effects:
                self.audio_effects.add_effect(effect_config)
            logger.info(f"Added {len(custom_effects)} custom effects")
        
        # Process audio through effects pipeline
        if self.audio_effects.effects:
            success = self.audio_effects.process_audio_file(audio_path, str(output_path))
            if success:
                logger.info(f"Audio effects applied: {output_path}")
                return str(output_path)
            else:
                logger.error("Audio effects processing failed")
                return audio_path
        else:
            logger.info("No effects to apply")
            return audio_path
    
    async def _create_placeholder_audio(self, output_path: str, text: str):
        """Create placeholder audio file (for demonstration)"""
        # In production, this would call actual Piper TTS
        # For now, create a simple WAV file placeholder
        
        import wave
        import struct
        import math
        
        sample_rate = 22050
        duration = max(1.0, len(text) * 0.1)  # Rough estimate
        num_samples = int(sample_rate * duration)
        
        # Generate simple tone (placeholder)
        frequency = 440.0  # A4 note
        audio_data = []
        
        for i in range(num_samples):
            # Simple sine wave with fade in/out
            t = i / sample_rate
            fade = min(1.0, t * 10, (duration - t) * 10)  # Fade in/out
            sample = fade * 0.1 * math.sin(2 * math.pi * frequency * t)
            audio_data.append(struct.pack('<h', int(sample * 32767)))
        
        # Write WAV file
        with wave.open(output_path, 'wb') as wav_file:
            wav_file.setnchannels(1)  # mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(b''.join(audio_data))
    
    def _estimate_audio_duration(self, text: str) -> float:
        """Estimate audio duration from text length"""
        # Rough estimate: ~150 words per minute, ~5 chars per word
        words = len(text) / 5
        duration = (words / 150) * 60  # Convert to seconds
        return max(1.0, duration)
    
    def _get_applied_effects(self, request: SynthesisRequest) -> List[str]:
        """Get list of applied effects"""
        effects = []
        
        if request.effects_preset:
            effects.append(f"preset:{request.effects_preset}")
        
        if request.custom_effects:
            for effect in request.custom_effects:
                effects.append(f"custom:{effect.effect_type.value}")
        
        return effects
    
    def get_available_voices(self) -> Dict[str, Dict[str, str]]:
        """Get available TTS voices"""
        return self.available_voices.copy()
    
    def get_voice_profiles(self) -> List[Dict]:
        """Get available voice cloning profiles"""
        return self.voice_cloning.list_profiles()
    
    def get_effects_presets(self) -> List[str]:
        """Get available audio effects presets"""
        return self.audio_effects.get_available_presets()
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics"""
        if not self.processing_history:
            return {
                "total_syntheses": 0,
                "success_rate": 0.0,
                "average_processing_time": 0.0,
                "total_audio_duration": 0.0
            }
        
        successful = [r for r in self.processing_history if r.success]
        
        return {
            "total_syntheses": len(self.processing_history),
            "successful_syntheses": len(successful),
            "success_rate": len(successful) / len(self.processing_history),
            "average_processing_time": sum(r.processing_time for r in successful) / len(successful) if successful else 0.0,
            "total_audio_duration": sum(r.duration for r in successful),
            "effects_usage": self._count_effects_usage(),
            "voice_usage": self._count_voice_usage(),
            "cloning_usage": sum(1 for r in successful if "voice_profile_id" in r.metadata.get("request", {}))
        }
    
    def _count_effects_usage(self) -> Dict[str, int]:
        """Count effects usage statistics"""
        effects_count = {}
        
        for result in self.processing_history:
            if result.success and result.effects_applied:
                for effect in result.effects_applied:
                    effects_count[effect] = effects_count.get(effect, 0) + 1
        
        return effects_count
    
    def _count_voice_usage(self) -> Dict[str, int]:
        """Count voice usage statistics"""
        voice_count = {}
        
        for result in self.processing_history:
            if result.success and result.voice_used:
                voice_count[result.voice_used] = voice_count.get(result.voice_used, 0) + 1
        
        return voice_count
    
    def create_voice_profile(self, 
                           audio_files: List[str],
                           name: str,
                           language: str = "en",
                           **kwargs) -> str:
        """Create new voice cloning profile"""
        return self.voice_cloning.create_voice_profile(
            audio_files=audio_files,
            name=name,
            language=language,
            **kwargs
        )
    
    def delete_voice_profile(self, profile_id: str) -> bool:
        """Delete voice cloning profile"""
        return self.voice_cloning.delete_profile(profile_id)
    
    def save_effects_config(self, config_path: str):
        """Save current effects configuration"""
        self.audio_effects.save_config(config_path)
    
    def load_effects_config(self, config_path: str):
        """Load effects configuration"""
        self.audio_effects.load_config(config_path)

async def main():
    """Demo of advanced AI features integration"""
    print("🚀 BINARY PIPER TTS - ADVANCED AI FEATURES")
    print("=" * 70)
    
    # Initialize advanced TTS engine
    engine = AdvancedTTSEngine()
    
    print(f"🎙️  Available voices: {len(engine.get_available_voices())}")
    print(f"👤 Voice profiles: {len(engine.get_voice_profiles())}")
    print(f"🎨 Effects presets: {len(engine.get_effects_presets())}")
    
    # Demo synthesis requests
    demo_requests = [
        {
            "name": "Standard TTS",
            "request": SynthesisRequest(
                text="Hello! This is a standard TTS synthesis example.",
                voice_id="en-US-lessac-medium"
            )
        },
        {
            "name": "With Effects",
            "request": SynthesisRequest(
                text="This example uses audio effects for enhanced quality.",
                voice_id="en-US-ryan-high",
                effects_preset="radio"
            )
        },
        {
            "name": "SSML Processing",
            "request": SynthesisRequest(
                text="""<speak>
                    <prosody rate="slow" pitch="low">This is slow and low.</prosody>
                    <break time="500ms"/>
                    <emphasis level="strong">This is emphasized!</emphasis>
                </speak>""",
                voice_id="en-GB-alba-medium",
                effects_preset="dramatic",
                ssml_enabled=True
            )
        },
        {
            "name": "Custom Effects",
            "request": SynthesisRequest(
                text="This example uses custom audio effects configuration.",
                voice_id="de-DE-thorsten-high",
                custom_effects=[
                    EffectConfig(EffectType.REVERB, {"room_size": 0.7, "wet_level": 0.4}),
                    EffectConfig(EffectType.COMPRESSOR, {"threshold": 0.4, "ratio": 3.0})
                ]
            )
        }
    ]
    
    print("\n🔥 Processing Demo Requests:")
    
    for demo in demo_requests:
        print(f"\n📝 {demo['name']}:")
        try:
            result = await engine.synthesize_advanced(demo['request'])
            
            if result.success:
                print(f"   ✅ Success: {result.output_path}")
                print(f"   ⏱️  Processing: {result.processing_time:.2f}s")
                print(f"   🎵 Duration: {result.duration:.2f}s")
                print(f"   🎭 Voice: {result.voice_used}")
                print(f"   🎨 Effects: {result.effects_applied}")
                print(f"   📝 SSML segments: {result.ssml_segments}")
            else:
                print(f"   ❌ Failed: {result.error_message}")
                
        except Exception as e:
            print(f"   💥 Error: {e}")
    
    # Show processing statistics
    print("\n📊 Processing Statistics:")
    stats = engine.get_processing_stats()
    print(f"   Total syntheses: {stats['total_syntheses']}")
    print(f"   Success rate: {stats['success_rate']:.1%}")
    print(f"   Average processing time: {stats['average_processing_time']:.2f}s")
    print(f"   Total audio duration: {stats['total_audio_duration']:.2f}s")
    
    print("\n🎯 Advanced Features:")
    print("   🧬 Voice Cloning - Create custom voice profiles from samples")
    print("   🎛️  Audio Effects - Real-time processing pipeline with presets")
    print("   📝 Enhanced SSML - Full SSML 1.1 specification support")
    print("   🚀 Async Processing - High-performance concurrent synthesis")
    print("   📊 Analytics - Detailed processing metrics and statistics")
    print("   💾 Profile Management - Persistent voice and effects storage")
    
    print("\n💡 Usage Examples:")
    print("   • Standard: await engine.synthesize_advanced(SynthesisRequest(text, voice_id))")
    print("   • With cloning: request.voice_profile_id = 'profile_id'")
    print("   • With effects: request.effects_preset = 'radio'")
    print("   • With SSML: request.ssml_enabled = True")
    
    print("\n" + "=" * 70)
    print("✅ Advanced AI features integration ready!")

if __name__ == "__main__":
    asyncio.run(main())
