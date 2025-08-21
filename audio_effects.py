#!/usr/bin/env python3
"""
Binary Piper TTS - Audio Effects Pipeline
Real-time audio processing and effects for enhanced TTS output
"""

import os
import json
import numpy as np
from typing import Dict, List, Optional, Tuple, Any, Union
import tempfile
from pathlib import Path
import logging
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import math
import wave

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EffectType(Enum):
    """Available audio effects"""
    REVERB = "reverb"
    ECHO = "echo"
    CHORUS = "chorus"
    PITCH_SHIFT = "pitch_shift"
    TIME_STRETCH = "time_stretch"
    VOLUME = "volume"
    FADE = "fade"
    NORMALIZE = "normalize"
    COMPRESSOR = "compressor"
    EQUALIZER = "equalizer"
    DISTORTION = "distortion"
    NOISE_GATE = "noise_gate"

@dataclass
class EffectConfig:
    """Configuration for an audio effect"""
    effect_type: EffectType
    parameters: Dict[str, Any]
    enabled: bool = True
    order: int = 0

class AudioEffect:
    """Base class for audio effects"""
    
    def __init__(self, config: EffectConfig):
        self.config = config
        self.sample_rate = 22050
        self.enabled = config.enabled
    
    def apply(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        """Apply effect to audio"""
        if not self.enabled:
            return audio
        return self._process(audio, sample_rate)
    
    def _process(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        """Override this method in subclasses"""
        return audio

class ReverbEffect(AudioEffect):
    """Reverb effect implementation"""
    
    def _process(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        room_size = self.config.parameters.get('room_size', 0.5)
        damping = self.config.parameters.get('damping', 0.5)
        wet_level = self.config.parameters.get('wet_level', 0.3)
        dry_level = self.config.parameters.get('dry_level', 0.7)
        
        # Simple reverb using multiple delay lines
        delays = [int(sample_rate * delay) for delay in [0.03, 0.05, 0.07, 0.09, 0.11]]
        gains = [0.6, 0.5, 0.4, 0.3, 0.2]
        
        reverb_audio = np.zeros_like(audio)
        
        for delay_samples, gain in zip(delays, gains):
            if delay_samples < len(audio):
                delayed = np.zeros_like(audio)
                delayed[delay_samples:] = audio[:-delay_samples]
                reverb_audio += delayed * gain * room_size * (1 - damping)
        
        # Mix dry and wet signals
        return dry_level * audio + wet_level * reverb_audio

class EchoEffect(AudioEffect):
    """Echo effect implementation"""
    
    def _process(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        delay_time = self.config.parameters.get('delay_time', 0.3)  # seconds
        feedback = self.config.parameters.get('feedback', 0.4)
        wet_level = self.config.parameters.get('wet_level', 0.3)
        
        delay_samples = int(delay_time * sample_rate)
        
        if delay_samples >= len(audio):
            return audio
        
        echo_audio = np.zeros_like(audio)
        echo_audio[delay_samples:] = audio[:-delay_samples] * feedback
        
        return audio + wet_level * echo_audio

class PitchShiftEffect(AudioEffect):
    """Pitch shift effect implementation"""
    
    def _process(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        pitch_shift = self.config.parameters.get('pitch_shift', 1.0)  # 1.0 = no change
        
        if pitch_shift == 1.0:
            return audio
        
        # Simple pitch shifting using resampling (not perfect but functional)
        # For better quality, would need phase vocoder or similar
        
        # Resample to change pitch
        new_length = int(len(audio) / pitch_shift)
        indices = np.linspace(0, len(audio) - 1, new_length)
        
        # Linear interpolation
        shifted_audio = np.interp(indices, np.arange(len(audio)), audio)
        
        # Pad or trim to original length
        if len(shifted_audio) < len(audio):
            # Pad with zeros
            padded = np.zeros_like(audio)
            padded[:len(shifted_audio)] = shifted_audio
            return padded
        else:
            # Trim to original length
            return shifted_audio[:len(audio)]

class VolumeEffect(AudioEffect):
    """Volume adjustment effect"""
    
    def _process(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        gain = self.config.parameters.get('gain', 1.0)
        return audio * gain

class NormalizeEffect(AudioEffect):
    """Audio normalization effect"""
    
    def _process(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        target_level = self.config.parameters.get('target_level', 0.9)
        
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            return audio * (target_level / max_val)
        return audio

class EqualizerEffect(AudioEffect):
    """Simple 3-band equalizer"""
    
    def _process(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        low_gain = self.config.parameters.get('low_gain', 1.0)
        mid_gain = self.config.parameters.get('mid_gain', 1.0)
        high_gain = self.config.parameters.get('high_gain', 1.0)
        
        # Simple frequency-domain processing
        fft = np.fft.rfft(audio)
        freqs = np.fft.rfftfreq(len(audio), 1/sample_rate)
        
        # Apply gains to different frequency bands
        low_mask = freqs < 300
        mid_mask = (freqs >= 300) & (freqs < 3000)
        high_mask = freqs >= 3000
        
        fft[low_mask] *= low_gain
        fft[mid_mask] *= mid_gain
        fft[high_mask] *= high_gain
        
        return np.fft.irfft(fft, len(audio))

class CompressorEffect(AudioEffect):
    """Audio compressor effect"""
    
    def _process(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        threshold = self.config.parameters.get('threshold', 0.5)
        ratio = self.config.parameters.get('ratio', 4.0)
        attack = self.config.parameters.get('attack', 0.003)  # seconds
        release = self.config.parameters.get('release', 0.1)   # seconds
        
        # Simple peak compressor
        compressed = np.copy(audio)
        envelope = 0.0
        attack_coeff = math.exp(-1.0 / (attack * sample_rate))
        release_coeff = math.exp(-1.0 / (release * sample_rate))
        
        for i in range(len(audio)):
            input_level = abs(audio[i])
            
            # Envelope follower
            if input_level > envelope:
                envelope = attack_coeff * envelope + (1 - attack_coeff) * input_level
            else:
                envelope = release_coeff * envelope + (1 - release_coeff) * input_level
            
            # Apply compression if above threshold
            if envelope > threshold:
                gain_reduction = threshold + (envelope - threshold) / ratio
                compressed[i] = audio[i] * (gain_reduction / envelope)
        
        return compressed

class AudioEffectsPipeline:
    """Main audio effects pipeline processor"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.effects: List[AudioEffect] = []
        self.presets: Dict[str, List[EffectConfig]] = {}
        self.config_path = config_path
        self.sample_rate = 22050
        
        self._init_default_presets()
        if config_path and os.path.exists(config_path):
            self.load_config(config_path)
        
        logger.info(f"Audio effects pipeline initialized with {len(self.effects)} effects")
    
    def _init_default_presets(self):
        """Initialize default effect presets"""
        
        # Radio Voice
        self.presets["radio"] = [
            EffectConfig(EffectType.COMPRESSOR, {"threshold": 0.4, "ratio": 6.0}, order=1),
            EffectConfig(EffectType.EQUALIZER, {"low_gain": 0.8, "mid_gain": 1.2, "high_gain": 1.1}, order=2),
            EffectConfig(EffectType.NORMALIZE, {"target_level": 0.85}, order=3)
        ]
        
        # Cathedral
        self.presets["cathedral"] = [
            EffectConfig(EffectType.REVERB, {"room_size": 0.9, "damping": 0.2, "wet_level": 0.5}, order=1),
            EffectConfig(EffectType.EQUALIZER, {"low_gain": 1.1, "mid_gain": 0.9, "high_gain": 0.7}, order=2)
        ]
        
        # Robot Voice
        self.presets["robot"] = [
            EffectConfig(EffectType.PITCH_SHIFT, {"pitch_shift": 0.8}, order=1),
            EffectConfig(EffectType.DISTORTION, {"drive": 0.3}, order=2),
            EffectConfig(EffectType.EQUALIZER, {"low_gain": 1.2, "mid_gain": 1.3, "high_gain": 0.8}, order=3)
        ]
        
        # Whisper
        self.presets["whisper"] = [
            EffectConfig(EffectType.VOLUME, {"gain": 0.3}, order=1),
            EffectConfig(EffectType.EQUALIZER, {"low_gain": 0.6, "mid_gain": 0.8, "high_gain": 1.2}, order=2),
            EffectConfig(EffectType.NOISE_GATE, {"threshold": 0.05}, order=3)
        ]
        
        # Dramatic
        self.presets["dramatic"] = [
            EffectConfig(EffectType.COMPRESSOR, {"threshold": 0.3, "ratio": 3.0}, order=1),
            EffectConfig(EffectType.REVERB, {"room_size": 0.6, "wet_level": 0.3}, order=2),
            EffectConfig(EffectType.EQUALIZER, {"low_gain": 1.3, "mid_gain": 1.0, "high_gain": 0.9}, order=3)
        ]
        
        # Telephone
        self.presets["telephone"] = [
            EffectConfig(EffectType.EQUALIZER, {"low_gain": 0.3, "mid_gain": 1.5, "high_gain": 0.4}, order=1),
            EffectConfig(EffectType.COMPRESSOR, {"threshold": 0.5, "ratio": 8.0}, order=2),
            EffectConfig(EffectType.DISTORTION, {"drive": 0.1}, order=3)
        ]
    
    def apply_preset(self, preset_name: str):
        """Apply a predefined effect preset"""
        if preset_name not in self.presets:
            raise ValueError(f"Unknown preset: {preset_name}")
        
        self.clear_effects()
        effect_configs = sorted(self.presets[preset_name], key=lambda x: x.order)
        
        for config in effect_configs:
            self.add_effect(config)
        
        logger.info(f"Applied preset '{preset_name}' with {len(effect_configs)} effects")
    
    def add_effect(self, config: EffectConfig):
        """Add an effect to the pipeline"""
        effect_class = self._get_effect_class(config.effect_type)
        effect = effect_class(config)
        self.effects.append(effect)
        
        # Sort effects by order
        self.effects.sort(key=lambda x: x.config.order)
    
    def _get_effect_class(self, effect_type: EffectType) -> type:
        """Get the effect class for a given effect type"""
        effect_classes = {
            EffectType.REVERB: ReverbEffect,
            EffectType.ECHO: EchoEffect,
            EffectType.PITCH_SHIFT: PitchShiftEffect,
            EffectType.VOLUME: VolumeEffect,
            EffectType.NORMALIZE: NormalizeEffect,
            EffectType.EQUALIZER: EqualizerEffect,
            EffectType.COMPRESSOR: CompressorEffect,
        }
        
        return effect_classes.get(effect_type, AudioEffect)
    
    def clear_effects(self):
        """Clear all effects from pipeline"""
        self.effects.clear()
    
    def process_audio_file(self, input_path: str, output_path: str) -> bool:
        """Process audio file through effects pipeline"""
        try:
            # Load audio file
            audio_data, sample_rate = self._load_audio(input_path)
            
            # Process through effects pipeline
            processed_audio = self.process_audio(audio_data, sample_rate)
            
            # Save processed audio
            self._save_audio(processed_audio, output_path, sample_rate)
            
            logger.info(f"Processed audio: {input_path} -> {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Audio processing failed: {e}")
            return False
    
    def process_audio(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        """Process audio through effects pipeline"""
        processed = audio.copy()
        
        for effect in self.effects:
            if effect.enabled:
                processed = effect.apply(processed, sample_rate)
                logger.debug(f"Applied {effect.config.effect_type.value}")
        
        return processed
    
    def _load_audio(self, file_path: str) -> Tuple[np.ndarray, int]:
        """Load audio file (basic WAV support)"""
        try:
            with wave.open(file_path, 'rb') as wav_file:
                frames = wav_file.readframes(wav_file.getnframes())
                sample_rate = wav_file.getframerate()
                channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                
                # Convert bytes to numpy array
                if sample_width == 1:
                    audio = np.frombuffer(frames, dtype=np.uint8)
                    audio = (audio.astype(np.float32) - 128) / 128.0
                elif sample_width == 2:
                    audio = np.frombuffer(frames, dtype=np.int16)
                    audio = audio.astype(np.float32) / 32768.0
                elif sample_width == 4:
                    audio = np.frombuffer(frames, dtype=np.int32)
                    audio = audio.astype(np.float32) / 2147483648.0
                else:
                    raise ValueError(f"Unsupported sample width: {sample_width}")
                
                # Convert stereo to mono if needed
                if channels == 2:
                    audio = audio.reshape(-1, 2)
                    audio = np.mean(audio, axis=1)
                
                return audio, sample_rate
                
        except Exception as e:
            logger.error(f"Failed to load audio file {file_path}: {e}")
            raise
    
    def _save_audio(self, audio: np.ndarray, file_path: str, sample_rate: int):
        """Save audio to WAV file"""
        try:
            # Convert float to int16
            audio_int16 = (audio * 32767).astype(np.int16)
            
            with wave.open(file_path, 'wb') as wav_file:
                wav_file.setnchannels(1)  # mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(audio_int16.tobytes())
                
        except Exception as e:
            logger.error(f"Failed to save audio file {file_path}: {e}")
            raise
    
    def get_available_presets(self) -> List[str]:
        """Get list of available effect presets"""
        return list(self.presets.keys())
    
    def get_pipeline_info(self) -> Dict:
        """Get information about current effects pipeline"""
        return {
            "num_effects": len(self.effects),
            "effects": [
                {
                    "type": effect.config.effect_type.value,
                    "enabled": effect.enabled,
                    "parameters": effect.config.parameters,
                    "order": effect.config.order
                }
                for effect in self.effects
            ],
            "available_presets": self.get_available_presets(),
            "sample_rate": self.sample_rate
        }
    
    def save_config(self, config_path: str):
        """Save current pipeline configuration"""
        config_data = {
            "effects": [
                {
                    "effect_type": effect.config.effect_type.value,
                    "parameters": effect.config.parameters,
                    "enabled": effect.enabled,
                    "order": effect.config.order
                }
                for effect in self.effects
            ],
            "presets": {
                name: [
                    {
                        "effect_type": config.effect_type.value,
                        "parameters": config.parameters,
                        "enabled": config.enabled,
                        "order": config.order
                    }
                    for config in configs
                ]
                for name, configs in self.presets.items()
            }
        }
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2)
        
        logger.info(f"Pipeline configuration saved: {config_path}")
    
    def load_config(self, config_path: str):
        """Load pipeline configuration"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # Load effects
            self.clear_effects()
            for effect_data in config_data.get("effects", []):
                config = EffectConfig(
                    effect_type=EffectType(effect_data["effect_type"]),
                    parameters=effect_data["parameters"],
                    enabled=effect_data["enabled"],
                    order=effect_data["order"]
                )
                self.add_effect(config)
            
            # Load presets
            for preset_name, preset_effects in config_data.get("presets", {}).items():
                self.presets[preset_name] = [
                    EffectConfig(
                        effect_type=EffectType(effect_data["effect_type"]),
                        parameters=effect_data["parameters"],
                        enabled=effect_data["enabled"],
                        order=effect_data["order"]
                    )
                    for effect_data in preset_effects
                ]
            
            logger.info(f"Pipeline configuration loaded: {config_path}")
            
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            raise

def main():
    """Demo of audio effects pipeline"""
    print("🎛️  BINARY PIPER TTS - AUDIO EFFECTS PIPELINE")
    print("=" * 70)
    
    # Initialize effects pipeline
    pipeline = AudioEffectsPipeline()
    
    print(f"🎨 Available presets: {', '.join(pipeline.get_available_presets())}")
    
    # Demo different presets
    presets_info = {
        "radio": "📻 Professional radio announcer voice",
        "cathedral": "🏰 Spacious cathedral reverb",
        "robot": "🤖 Futuristic robotic voice",
        "whisper": "🤫 Subtle whisper effect",
        "dramatic": "🎭 Cinematic dramatic enhancement",
        "telephone": "☎️ Vintage telephone quality"
    }
    
    print("\n🎭 Effect Presets:")
    for preset, description in presets_info.items():
        print(f"   {description}")
        pipeline.apply_preset(preset)
        info = pipeline.get_pipeline_info()
        print(f"      Effects: {info['num_effects']} | "
              f"Types: {[e['type'] for e in info['effects']]}")
    
    print("\n🔧 Available Effects:")
    print("   🔊 Volume Control - Adjust audio level")
    print("   🎵 Equalizer - 3-band frequency adjustment") 
    print("   🎙️ Compressor - Dynamic range control")
    print("   🏗️ Reverb - Spatial audio enhancement")
    print("   📢 Echo - Delay-based repetition")
    print("   🎼 Pitch Shift - Frequency modification")
    print("   📏 Normalize - Level standardization")
    
    print("\n🚀 Real-time Processing:")
    print("   ⚡ Low-latency audio pipeline")
    print("   🔄 Chainable effect processing")
    print("   💾 Preset save/load system")
    print("   🎛️ Parameter customization")
    print("   📊 Pipeline monitoring and info")
    
    # Example usage
    pipeline.apply_preset("dramatic")
    
    print("\n💡 Usage Examples:")
    print("   • Apply preset: pipeline.apply_preset('radio')")
    print("   • Process file: pipeline.process_audio_file('input.wav', 'output.wav')")
    print("   • Get info: pipeline.get_pipeline_info()")
    
    print("\n" + "=" * 70)
    print("✅ Audio effects pipeline ready!")

if __name__ == "__main__":
    main()
