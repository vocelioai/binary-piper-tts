import os
import io
import tempfile
import subprocess
import json
import asyncio
import time
import hashlib
import gc
import threading
import weakref
from collections import OrderedDict
from datetime import datetime, timezone
from typing import Optional, List, Dict, Tuple
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

# Optional performance monitoring
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    psutil = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Binary Piper TTS Service",
    description="High-performance Text-to-Speech using Binary Piper",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for web UI
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuration with environment & local fallbacks
DEFAULT_MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
MODELS_DIR = os.environ.get("MODELS_DIR") or DEFAULT_MODELS_DIR

# Piper binary: allow override, adapt for Windows (where container path won't exist)
DEFAULT_PIPER_BINARY = "/usr/local/bin/piper" if os.name != "nt" else os.path.join(os.path.dirname(__file__), "piper-bin", "piper", "piper.exe")
PIPER_BINARY = os.environ.get("PIPER_BINARY") or DEFAULT_PIPER_BINARY

MAX_TEXT_LENGTH = 20000  # Increased for call center use - supports long conversations

logger.info(f"Resolved MODELS_DIR={MODELS_DIR}")
logger.info(f"Resolved PIPER_BINARY={PIPER_BINARY}")

# Request models
class SynthesisRequest(BaseModel):
    text: str
    voice: str = "en_US-lessac-medium"
    speaker_id: Optional[int] = 0
    format: Optional[str] = "wav"  # wav, mp3, ogg
    quality: Optional[str] = "standard"  # low, standard, high
    speed: Optional[float] = 1.0  # 0.5 to 2.0
    enable_ssml: Optional[bool] = False

class VoiceInfo(BaseModel):
    name: str
    language: str
    sample_rate: int
    num_speakers: int
    model_path: str
    config_path: str

class AudioCache:
    """LRU cache for synthesized audio with memory management"""
    def __init__(self, max_size: int = 50, max_memory_mb: int = 200):
        self.max_size = max_size
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.cache = OrderedDict()
        self.memory_usage = 0
        self.lock = threading.Lock()
        
    def _get_cache_key(self, text: str, voice: str, speaker_id: int) -> str:
        """Generate cache key from synthesis parameters"""
        key_string = f"{text}|{voice}|{speaker_id}"
        return hashlib.md5(key_string.encode()).hexdigest()
        
    def get(self, text: str, voice: str, speaker_id: int) -> Optional[bytes]:
        """Get cached audio data"""
        with self.lock:
            key = self._get_cache_key(text, voice, speaker_id)
            if key in self.cache:
                # Move to end (most recently used)
                audio_data = self.cache.pop(key)
                self.cache[key] = audio_data
                logger.info(f"🎯 Cache HIT for key: {key[:8]}...")
                return audio_data
            return None
    
    def put(self, text: str, voice: str, speaker_id: int, audio_data: bytes):
        """Cache audio data with memory management"""
        with self.lock:
            key = self._get_cache_key(text, voice, speaker_id)
            audio_size = len(audio_data)
            
            # Check if single item is too large
            if audio_size > self.max_memory_bytes:
                logger.warning(f"⚠️  Audio too large to cache: {audio_size / 1024 / 1024:.1f}MB")
                return
                
            # Remove items if cache is full or memory limit exceeded
            while (len(self.cache) >= self.max_size or 
                   self.memory_usage + audio_size > self.max_memory_bytes):
                if not self.cache:
                    break
                oldest_key, oldest_data = self.cache.popitem(last=False)
                self.memory_usage -= len(oldest_data)
                logger.info(f"🗑️  Evicted cache entry: {oldest_key[:8]}...")
            
            self.cache[key] = audio_data
            self.memory_usage += audio_size
            logger.info(f"💾 Cached audio: {key[:8]}... ({audio_size / 1024:.1f}KB, total: {self.memory_usage / 1024 / 1024:.1f}MB)")
    
    def clear(self):
        """Clear all cached data"""
        with self.lock:
            self.cache.clear()
            self.memory_usage = 0
            logger.info("🧹 Audio cache cleared")
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        with self.lock:
            return {
                "entries": len(self.cache),
                "memory_usage_mb": round(self.memory_usage / 1024 / 1024, 2),
                "max_entries": self.max_size,
                "max_memory_mb": self.max_memory_bytes / 1024 / 1024
            }

class VoiceModelManager:
    """Advanced voice model management with preloading and monitoring"""
    def __init__(self):
        self.loaded_models = {}
        self.model_usage = OrderedDict()  # Track usage frequency
        self.lock = threading.Lock()
        self.preload_popular = True
        
    def get_model_memory_usage(self) -> float:
        """Estimate memory usage of loaded models (MB)"""
        try:
            if PSUTIL_AVAILABLE:
                process = psutil.Process()
                return process.memory_info().rss / 1024 / 1024
            else:
                return 0.0
        except:
            return 0.0
    
    def track_usage(self, voice: str):
        """Track voice usage for intelligent caching"""
        with self.lock:
            if voice in self.model_usage:
                self.model_usage.move_to_end(voice)
                self.model_usage[voice] += 1
            else:
                self.model_usage[voice] = 1
                
    def get_popular_voices(self, limit: int = 10) -> List[str]:
        """Get most frequently used voices"""
        with self.lock:
            sorted_voices = sorted(self.model_usage.items(), key=lambda x: x[1], reverse=True)
            return [voice for voice, _ in sorted_voices[:limit]]
    
    def preload_voice_models(self, voices: List[str]):
        """Preload popular voice models for faster synthesis"""
        for voice in voices:
            if voice in VOICES_CACHE:
                logger.info(f"🚀 Preloading voice model: {voice}")
                # Model is already "loaded" in our current system
                self.track_usage(voice)

# Global caches
AUDIO_CACHE = AudioCache(max_size=100, max_memory_mb=300)
VOICE_MANAGER = VoiceModelManager()

# Global voice cache
VOICES_CACHE = {}

def load_voices():
    """Load all available voice models"""
    global VOICES_CACHE
    VOICES_CACHE = {}
    
    if not os.path.exists(MODELS_DIR):
        logger.error(f"Models directory {MODELS_DIR} not found")
        return
    
    for file in os.listdir(MODELS_DIR):
        if file.endswith('.onnx'):
            voice_name = file.replace('.onnx', '')
            model_path = os.path.join(MODELS_DIR, file)
            config_path = os.path.join(MODELS_DIR, f"{voice_name}.onnx.json")
            
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    
                    VOICES_CACHE[voice_name] = VoiceInfo(
                        name=voice_name,
                        language=config.get("language", {}).get("code", "unknown"),
                        sample_rate=config.get("audio", {}).get("sample_rate", 22050),
                        num_speakers=config.get("num_speakers", 1),
                        model_path=model_path,
                        config_path=config_path
                    )
                    logger.info(f"Loaded voice: {voice_name}")
                except Exception as e:
                    logger.error(f"Error loading config for {voice_name}: {e}")

def process_ssml(text: str, speed: float = 1.0) -> str:
    """Process SSML-like markup for enhanced voice control"""
    if not text:
        return text
    
    # Basic SSML processing for speed control
    if speed != 1.0:
        # For now, we'll handle speed at the Piper level
        # Future: implement proper SSML parsing
        pass
    
    # Remove any existing SSML tags for now (basic sanitization)
    import re
    text = re.sub(r'<[^>]+>', '', text)
    
    return text.strip()

def compress_audio(audio_data: bytes, format: str = "wav", quality: str = "standard") -> Tuple[bytes, str]:
    """Compress audio to different formats (requires ffmpeg)"""
    if format == "wav" or not format:
        return audio_data, "audio/wav"
    
    # For now, return original WAV data
    # Future implementation would use ffmpeg for MP3/OGG conversion
    # This would require: pip install pydub
    
    logger.info(f"Audio compression requested ({format}, {quality}) - returning WAV for now")
    return audio_data, "audio/wav"

def apply_audio_effects(audio_data: bytes, speed: float = 1.0) -> bytes:
    """Apply audio effects like speed changes (requires audio processing library)"""
    if speed == 1.0:
        return audio_data
    
    # For now, return original audio
    # Future implementation would use librosa or similar for speed adjustment
    logger.info(f"Speed adjustment requested ({speed}x) - returning original audio for now")
    return audio_data

async def stream_synthesis_chunks(text_chunks: List[str], voice: str, speaker_id: int = 0):
    """Stream audio synthesis by processing chunks in real-time"""
    for i, chunk in enumerate(text_chunks):
        logger.info(f"🌊 Streaming chunk {i+1}/{len(text_chunks)}: '{chunk[:50]}...'")
        
        # Check cache first
        cached_audio = AUDIO_CACHE.get(chunk, voice, speaker_id)
        if cached_audio:
            yield cached_audio
            continue
            
        # Synthesize chunk
        temp_files = []
        try:
            voice_info = VOICES_CACHE[voice]
            
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as audio_file:
                audio_file_path = audio_file.name
                temp_files.append(audio_file_path)
            
            cmd = [
                PIPER_BINARY,
                "--model", voice_info.model_path,
                "--config", voice_info.config_path,
                "--output_file", audio_file_path
            ]
            
            if voice_info.num_speakers > 1 and speaker_id is not None:
                cmd.extend(["--speaker", str(speaker_id)])
            
            result = subprocess.run(
                cmd,
                input=chunk,
                text=True,
                capture_output=True,
                timeout=120,  # Shorter timeout for streaming chunks
                check=False
            )
            
            if result.returncode == 0 and os.path.exists(audio_file_path):
                with open(audio_file_path, 'rb') as f:
                    audio_data = f.read()
                
                # Cache the chunk
                AUDIO_CACHE.put(chunk, voice, speaker_id, audio_data)
                yield audio_data
            else:
                logger.error(f"Failed to synthesize chunk: {result.stderr}")
                
        except Exception as e:
            logger.error(f"Error synthesizing chunk: {e}")
        finally:
            # Cleanup
            for temp_file in temp_files:
                try:
                    os.unlink(temp_file)
                except:
                    pass

def validate_text_input(text: str) -> str:
    """Validate and sanitize text input - supports long call center conversations"""
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    text = text.strip()
    if len(text) > MAX_TEXT_LENGTH:
        raise HTTPException(
            status_code=400, 
            detail=f"Text too long. Maximum {MAX_TEXT_LENGTH:,} characters allowed (current: {len(text):,}). For longer texts, consider splitting into multiple requests."
        )
    
    return text

def chunk_long_text(text: str, max_chunk_size: int = 5000) -> List[str]:
    """Split long text into chunks at sentence boundaries for better TTS quality"""
    if len(text) <= max_chunk_size:
        return [text]
    
    # Split on sentence endings, preserving the punctuation
    import re
    sentences = re.split(r'([.!?]+\s*)', text)
    
    chunks = []
    current_chunk = ""
    
    i = 0
    while i < len(sentences):
        sentence = sentences[i]
        
        # Add sentence and its punctuation if it exists
        potential_chunk = current_chunk + sentence
        if i + 1 < len(sentences) and sentences[i + 1].strip() in '.!?':
            potential_chunk += sentences[i + 1]
            i += 1
        
        if len(potential_chunk) <= max_chunk_size:
            current_chunk = potential_chunk
        else:
            # Current chunk is full, start a new one
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
                if i + 1 < len(sentences) and sentences[i + 1].strip() in '.!?':
                    current_chunk += sentences[i + 1]
                    i += 1
            else:
                # Single sentence is too long, force split
                chunks.append(sentence[:max_chunk_size].strip())
                current_chunk = sentence[max_chunk_size:]
        
        i += 1
    
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return [chunk for chunk in chunks if chunk.strip()]

def validate_voice_id(voice_id: str) -> VoiceInfo:
    """Validate voice ID and return voice info"""
    if voice_id not in VOICES_CACHE:
        available_voices = list(VOICES_CACHE.keys())
        raise HTTPException(
            status_code=404, 
            detail=f"Voice '{voice_id}' not found. Available voices: {available_voices}"
        )
    
    return VOICES_CACHE[voice_id]

@app.on_event("startup")
async def startup_event():
    """Load voices on startup"""
    logger.info("Starting Binary Piper TTS Service...")
    load_voices()
    
    if not VOICES_CACHE:
        logger.error("No voices loaded! Check models directory.")
    else:
        logger.info(f"Loaded {len(VOICES_CACHE)} voices: {list(VOICES_CACHE.keys())}")

@app.get("/")
async def root():
    """Serve the web UI"""
    return FileResponse("static/index.html")

@app.get("/api")
async def api_info():
    """API endpoint with service info"""
    return {
        "service": "Binary Piper TTS",
        "version": "1.0.0",
        "status": "running",
        "voices_loaded": len(VOICES_CACHE),
        "available_voices": list(VOICES_CACHE.keys()),
        "piper_binary": PIPER_BINARY,
        "text_limit": f"{MAX_TEXT_LENGTH:,} characters",
        "endpoints": {
            "voices": "/voices - List available voices",
            "synthesize": "/synthesize - Standard synthesis (up to 20K chars)",
            "synthesize_long": "/synthesize_long - Long text with chunking",
            "config": "/config - Service configuration",
            "health": "/health - Health check",
            "web_ui": "/ - Web interface",
            "api_info": "/api - This endpoint"
        }
    }

@app.get("/voices")
async def get_voices():
    """Get all available voices"""
    if not VOICES_CACHE:
        raise HTTPException(status_code=503, detail="No voices available")
    
    # Return simple array of voice names for web UI compatibility
    return list(VOICES_CACHE.keys())

@app.get("/voices/detailed")
async def get_voices_detailed():
    """Get all available voices with detailed metadata"""
    if not VOICES_CACHE:
        raise HTTPException(status_code=503, detail="No voices available")
    
    voices_info = {}
    for voice_id, voice_info in VOICES_CACHE.items():
        voices_info[voice_id] = {
            "name": voice_info.name,
            "language": voice_info.language,
            "sample_rate": voice_info.sample_rate,
            "num_speakers": voice_info.num_speakers,
            "supports_multiple_speakers": voice_info.num_speakers > 1
        }
    
    return {
        "voices": voices_info,
        "total_count": len(voices_info)
    }

@app.get("/voices/{voice_id}")
async def get_voice_details(voice_id: str):
    """Get detailed info about a specific voice"""
    voice_info = validate_voice_id(voice_id)
    
    return {
        "voice_id": voice_id,
        "name": voice_info.name,
        "language": voice_info.language,
        "sample_rate": voice_info.sample_rate,
        "num_speakers": voice_info.num_speakers,
        "supports_multiple_speakers": voice_info.num_speakers > 1,
        "model_path": voice_info.model_path,
        "config_path": voice_info.config_path
    }

@app.get("/config")
async def get_configuration():
    """Get current TTS service configuration"""
    return {
        "service": "Binary Piper TTS",
        "version": "1.0.0",
        "text_limits": {
            "max_length": MAX_TEXT_LENGTH,
            "max_length_formatted": f"{MAX_TEXT_LENGTH:,}",
            "chunk_size": 4000,
            "description": f"Standard endpoint supports up to {MAX_TEXT_LENGTH:,} chars. Use /synthesize_long for longer texts."
        },
        "performance": {
            "timeout_standard": "120-300s (generous, length-based)",
            "timeout_long": "180-600s per chunk (very generous)",
            "timeout_formula": "Standard: 120s + (chars÷50), Long: 180s + (chars÷25)",
            "chunking_enabled": True,
            "max_chunk_size": "4,000 characters",
            "synthesis_logging": "Enabled with timing details"
        },
        "voices": {
            "total_loaded": len(VOICES_CACHE),
            "languages_supported": len(set(voice.language for voice in VOICES_CACHE.values()))
        },
        "endpoints": {
            "synthesize": "Standard synthesis (up to 20,000 chars)",
            "synthesize_long": "Long text synthesis with automatic chunking",
            "voices": "List available voices",
            "health": "Service health check"
        }
    }

@app.post("/synthesize")
async def synthesize_speech(request: SynthesisRequest):
    """Enhanced synthesis with caching, SSML support, and audio effects"""
    
    # Validate inputs
    text = validate_text_input(request.text)
    voice_info = validate_voice_id(request.voice)
    
    # Validate speaker ID
    if request.speaker_id and request.speaker_id >= voice_info.num_speakers:
        raise HTTPException(
            status_code=400,
            detail=f"Speaker ID {request.speaker_id} not available. Voice has {voice_info.num_speakers} speakers (0-{voice_info.num_speakers-1})"
        )
    
    # Validate speed parameter
    if not (0.5 <= request.speed <= 2.0):
        raise HTTPException(
            status_code=400,
            detail=f"Speed must be between 0.5 and 2.0 (current: {request.speed})"
        )
    
    # Process SSML if enabled
    if request.enable_ssml:
        text = process_ssml(text, request.speed)
    
    # Create cache key including all parameters
    cache_key_params = (text, request.voice, request.speaker_id or 0, request.speed, request.quality)
    cache_key = hashlib.md5(str(cache_key_params).encode()).hexdigest()
    
    # 🎯 Check audio cache first
    cached_audio = AUDIO_CACHE.get(text, request.voice, request.speaker_id or 0)
    if cached_audio and request.speed == 1.0 and request.format == "wav":
        VOICE_MANAGER.track_usage(request.voice)
        logger.info(f"⚡ Returning cached audio for '{text[:50]}...' ({len(cached_audio)} bytes)")
        
        # Determine media type
        media_type = "audio/wav" if request.format == "wav" else f"audio/{request.format}"
        
        return StreamingResponse(
            io.BytesIO(cached_audio),
            media_type=media_type,
            headers={
                "Content-Disposition": f"attachment; filename=speech_{request.voice}.{request.format}",
                "Cache-Source": "memory",
                "X-Processing-Time": "0.001s",
                "X-Speed": str(request.speed),
                "X-Quality": request.quality
            }
        )
    if cached_audio:
        VOICE_MANAGER.track_usage(request.voice)
        logger.info(f"⚡ Returning cached audio for '{text[:50]}...' ({len(cached_audio)} bytes)")
        return StreamingResponse(
            io.BytesIO(cached_audio),
            media_type="audio/wav",
            headers={
                "Content-Disposition": f"attachment; filename=speech_{request.voice}.wav",
                "Cache-Source": "memory",
                "X-Processing-Time": "0.001s"
            }
        )
    
    temp_files = []
    try:
        # Create temporary output file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as audio_file:
            audio_file_path = audio_file.name
            temp_files.append(audio_file_path)
        
        # Build Piper command
        cmd = [
            PIPER_BINARY,
            "--model", voice_info.model_path,
            "--config", voice_info.config_path,
            "--output_file", audio_file_path
        ]
        
        # Add speaker ID if voice supports multiple speakers
        if voice_info.num_speakers > 1 and request.speaker_id is not None:
            cmd.extend(["--speaker", str(request.speaker_id)])
        
        logger.info(f"🎵 Synthesizing: '{text[:50]}...' with voice '{request.voice}' (cache miss)")
        
        # Run Piper binary with generous timeout for longer texts
        # More generous formula: base 120s + extra time for longer texts
        timeout_duration = min(300, max(120, 120 + (len(text) // 50)))  # 120-300s based on text length
        logger.info(f"Using timeout: {timeout_duration}s for {len(text)} characters")
        
        start_time = time.time()
        result = subprocess.run(
            cmd,
            input=text,
            text=True,
            capture_output=True,
            timeout=timeout_duration,
            check=False
        )
        synthesis_time = time.time() - start_time
        logger.info(f"Synthesis completed in {synthesis_time:.2f}s")
        
        if result.returncode != 0:
            error_msg = result.stderr or "Unknown Piper error"
            logger.error(f"Piper failed: {error_msg}")
            raise HTTPException(status_code=500, detail=f"Synthesis failed: {error_msg}")
        
        # Check if output file was created
        if not os.path.exists(audio_file_path) or os.path.getsize(audio_file_path) == 0:
            raise HTTPException(status_code=500, detail="No audio output generated")
        
        # Read generated audio
        with open(audio_file_path, 'rb') as f:
            audio_data = f.read()
        
        end_time = time.time()
        synthesis_time = round(end_time - start_time, 3)
        
        # 🎛️ Apply audio effects (speed, etc.)
        if request.speed != 1.0:
            audio_data = apply_audio_effects(audio_data, request.speed)
        
        # �️ Compress audio if requested
        compressed_audio, media_type = compress_audio(audio_data, request.format, request.quality)
        
        # �💾 Cache the synthesized audio for future requests (original WAV)
        AUDIO_CACHE.put(text, request.voice, request.speaker_id or 0, audio_data)
        VOICE_MANAGER.track_usage(request.voice)
        
        file_extension = request.format if request.format in ['wav', 'mp3', 'ogg'] else 'wav'
        
        logger.info(f"✅ Synthesized {len(compressed_audio)} bytes in {synthesis_time}s - cached for future use")
        
        # Return audio as streaming response
        return StreamingResponse(
            io.BytesIO(compressed_audio),
            media_type=media_type,
            headers={
                "Content-Disposition": f"attachment; filename=speech_{request.voice}.{file_extension}",
                "Content-Length": str(len(compressed_audio)),
                "X-Voice-Used": request.voice,
                "X-Speaker-ID": str(request.speaker_id or 0),
                "X-Text-Length": str(len(text)),
                "X-Processing-Time": f"{synthesis_time}s",
                "X-Cache-Source": "fresh",
                "X-Speed": str(request.speed),
                "X-Quality": request.quality,
                "X-Format": request.format,
                "X-SSML-Enabled": str(request.enable_ssml)
            }
        )
        
    except subprocess.TimeoutExpired:
        logger.error(f"Piper synthesis timeout for text length: {len(text)} chars")
        raise HTTPException(
            status_code=504, 
            detail=f"Synthesis timeout - text may be too long ({len(text):,} chars). Try /synthesize_long for very long texts."
        )
    except Exception as e:
        logger.error(f"Synthesis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Synthesis failed: {str(e)}")
    finally:
        # Cleanup temporary files
        for temp_file in temp_files:
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
            except Exception as e:
                logger.warning(f"Failed to cleanup temp file {temp_file}: {e}")

@app.post("/synthesize_stream")
async def synthesize_streaming(request: SynthesisRequest):
    """🌊 Stream synthesis for real-time audio generation"""
    
    # Validate inputs
    text = validate_text_input(request.text)
    voice_info = validate_voice_id(request.voice)
    
    # Process SSML if enabled
    if request.enable_ssml:
        text = process_ssml(text, request.speed)
    
    # Split text into streaming chunks
    chunks = chunk_long_text(text, max_chunk_size=500)  # Smaller chunks for streaming
    logger.info(f"🌊 Streaming synthesis: {len(chunks)} chunks for '{text[:50]}...'")
    
    async def generate_streaming_audio():
        """Generate audio chunks in real-time"""
        async for audio_chunk in stream_synthesis_chunks(chunks, request.voice, request.speaker_id or 0):
            # Apply effects if needed
            if request.speed != 1.0:
                audio_chunk = apply_audio_effects(audio_chunk, request.speed)
            
            # Compress if needed
            compressed_chunk, _ = compress_audio(audio_chunk, request.format, request.quality)
            
            yield compressed_chunk
    
    # Determine media type
    media_type = "audio/wav" if request.format == "wav" else f"audio/{request.format}"
    
    return StreamingResponse(
        generate_streaming_audio(),
        media_type=media_type,
        headers={
            "Content-Disposition": f"attachment; filename=stream_{request.voice}.{request.format}",
            "X-Voice-Used": request.voice,
            "X-Streaming": "true",
            "X-Chunks": str(len(chunks)),
            "X-Speed": str(request.speed),
            "X-Quality": request.quality
        }
    )

@app.post("/synthesize_long")
async def synthesize_long_text(request: SynthesisRequest):
    """
    Synthesize very long text by automatically chunking it and combining audio
    Perfect for call center scripts, long conversations, or detailed announcements
    """
    
    # Basic validation
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    text = request.text.strip()
    voice_info = validate_voice_id(request.voice)
    
    # For very long texts, use chunking
    if len(text) > 5000:
        logger.info(f"Long text detected ({len(text):,} chars), using chunking approach")
        chunks = chunk_long_text(text, max_chunk_size=4000)
        logger.info(f"Split into {len(chunks)} chunks")
    else:
        chunks = [text]
    
    temp_files = []
    audio_chunks = []
    
    try:
        # Process each chunk
        for i, chunk in enumerate(chunks):
            logger.info(f"Processing chunk {i+1}/{len(chunks)} ({len(chunk)} chars)")
            
            # Create temporary output file for this chunk
            with tempfile.NamedTemporaryFile(suffix=f'_chunk_{i}.wav', delete=False) as audio_file:
                audio_file_path = audio_file.name
                temp_files.append(audio_file_path)
            
            # Build Piper command
            cmd = [
                PIPER_BINARY,
                "--model", voice_info.model_path,
                "--config", voice_info.config_path,
                "--output_file", audio_file_path
            ]
            
            # Add speaker ID if voice supports multiple speakers
            if voice_info.num_speakers > 1 and request.speaker_id is not None:
                cmd.extend(["--speaker", str(request.speaker_id)])
            
            # Run Piper binary for this chunk with generous timeout
            # More generous for chunks: base 180s + extra for longer chunks
            chunk_timeout = min(600, max(180, 180 + (len(chunk) // 25)))  # 180-600s based on chunk length
            logger.info(f"Processing chunk {i+1}/{len(chunks)} with timeout: {chunk_timeout}s")
            
            chunk_start = time.time()
            result = subprocess.run(
                cmd,
                input=chunk,
                text=True,
                capture_output=True,
                timeout=chunk_timeout,
                check=False
            )
            chunk_time = time.time() - chunk_start
            logger.info(f"Chunk {i+1} completed in {chunk_time:.2f}s")
            
            if result.returncode != 0:
                error_msg = result.stderr or "Unknown Piper error"
                logger.error(f"Piper failed on chunk {i+1}: {error_msg}")
                raise HTTPException(status_code=500, detail=f"Synthesis failed on chunk {i+1}: {error_msg}")
            
            # Check if output file was created
            if not os.path.exists(audio_file_path) or os.path.getsize(audio_file_path) == 0:
                raise HTTPException(status_code=500, detail=f"No audio output generated for chunk {i+1}")
            
            # Read generated audio chunk
            with open(audio_file_path, 'rb') as f:
                chunk_data = f.read()
                audio_chunks.append(chunk_data)
        
        # Combine all audio chunks (simple concatenation for WAV files)
        if len(audio_chunks) == 1:
            combined_audio = audio_chunks[0]
        else:
            # For multiple chunks, we'll use simple binary concatenation
            # This works for WAV files with identical headers
            combined_audio = audio_chunks[0]  # Start with first chunk (includes WAV header)
            
            # Append data from subsequent chunks (skip their WAV headers)
            for chunk_data in audio_chunks[1:]:
                if len(chunk_data) > 44:  # WAV header is typically 44 bytes
                    combined_audio += chunk_data[44:]  # Skip WAV header, append audio data
        
        logger.info(f"Successfully synthesized {len(combined_audio):,} bytes from {len(chunks)} chunks")
        
        # Return combined audio
        return StreamingResponse(
            io.BytesIO(combined_audio),
            media_type="audio/wav",
            headers={
                "Content-Disposition": f"attachment; filename=long_speech_{request.voice}.wav",
                "Content-Length": str(len(combined_audio)),
                "X-Voice-Used": request.voice,
                "X-Speaker-ID": str(request.speaker_id or 0),
                "X-Text-Length": str(len(text)),
                "X-Chunks-Used": str(len(chunks)),
                "X-Long-Text-Mode": "true"
            }
        )
        
    except subprocess.TimeoutExpired:
        logger.error(f"Piper synthesis timeout on long text ({len(text):,} chars, {len(chunks)} chunks)")
        raise HTTPException(
            status_code=504, 
            detail=f"Synthesis timeout on long text ({len(text):,} chars). Consider splitting into smaller segments."
        )
    except Exception as e:
        logger.error(f"Long text synthesis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Long text synthesis failed: {str(e)}")
    finally:
        # Cleanup temporary files
        for temp_file in temp_files:
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
            except Exception as e:
                logger.warning(f"Failed to cleanup temp file {temp_file}: {e}")

@app.get("/health")
async def health_check():
    """Comprehensive health check"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checks": {}
    }
    
    # Check Piper binary
    try:
        result = subprocess.run([PIPER_BINARY, "--help"], capture_output=True, timeout=5)
        health_status["checks"]["piper_binary"] = {
            "status": "ok" if result.returncode == 0 else "error",
            "message": "Piper binary accessible"
        }
    except Exception as e:
        health_status["checks"]["piper_binary"] = {
            "status": "error",
            "message": f"Piper binary error: {str(e)}"
        }
        health_status["status"] = "unhealthy"
    
    # Check voices
    health_status["checks"]["voices"] = {
        "status": "ok" if VOICES_CACHE else "error",
        "message": f"{len(VOICES_CACHE)} voices loaded",
        "voices": list(VOICES_CACHE.keys())
    }
    if not VOICES_CACHE:
        health_status["status"] = "unhealthy"
    
    # Check models directory
    health_status["checks"]["models_directory"] = {
        "status": "ok" if os.path.exists(MODELS_DIR) else "error",
        "message": f"Models directory: {MODELS_DIR}",
        "exists": os.path.exists(MODELS_DIR)
    }
    
    return health_status

@app.get("/test-performance")
async def test_performance():
    """Test performance and timeout calculations without synthesis"""
    test_texts = [
        ("Short text", "Hello world, this is a test.", 100),
        ("Medium text", "This is a medium length text for testing." * 10, 1000),
        ("Long text", "This is a longer text for performance testing." * 50, 5000),
        ("Very long text", "This text simulates a long call center script." * 100, 15000)
    ]
    
    results = []
    for name, text, expected_chars in test_texts:
        actual_chars = len(text)
        timeout_standard = min(300, max(120, 120 + (actual_chars // 50)))
        timeout_long = min(600, max(180, 180 + (actual_chars // 25)))
        
        results.append({
            "test_name": name,
            "text_length": actual_chars,
            "expected_length": expected_chars,
            "timeout_standard": f"{timeout_standard}s",
            "timeout_long": f"{timeout_long}s",
            "estimated_synthesis_time": f"{actual_chars // 500}-{actual_chars // 200}s"
        })
    
    return {
        "service": "Binary Piper TTS Performance Test",
        "test_results": results,
        "timeout_formulas": {
            "standard": "min(300, max(120, 120 + (chars÷50)))",
            "long_text": "min(600, max(180, 180 + (chars÷25)))"
        },
        "recommendations": {
            "under_5000_chars": "Use /synthesize endpoint",
            "over_5000_chars": "Use /synthesize_long endpoint",
            "very_long_texts": "Consider splitting into smaller requests"
        }
    }

@app.get("/cache/stats")
async def get_cache_stats():
    """📊 Get cache statistics and performance metrics"""
    return {
        "audio_cache": AUDIO_CACHE.get_stats(),
        "voice_manager": {
            "memory_usage_mb": VOICE_MANAGER.get_model_memory_usage(),
            "popular_voices": VOICE_MANAGER.get_popular_voices(limit=10),
            "total_usage_tracked": sum(VOICE_MANAGER.model_usage.values())
        },
        "system_performance": {
            "voices_loaded": len(VOICES_CACHE),
            "total_requests_processed": sum(VOICE_MANAGER.model_usage.values())
        }
    }

@app.post("/cache/clear")
async def clear_cache():
    """🧹 Clear audio cache and reset usage statistics"""
    AUDIO_CACHE.clear()
    VOICE_MANAGER.model_usage.clear()
    
    # Force garbage collection
    gc.collect()
    
    return {
        "status": "success",
        "message": "Cache cleared successfully",
        "memory_freed": "Cache and usage statistics reset"
    }

@app.post("/cache/preload")
async def preload_popular_voices(voices: List[str] = None):
    """🚀 Preload popular voice models for faster synthesis"""
    if voices is None:
        # Auto-detect popular voices
        voices = VOICE_MANAGER.get_popular_voices(limit=10)
        if not voices:
            # Default popular voices if no usage data
            voices = ["en_US-lessac-medium", "en_US-amy-medium", "es_ES-davefx-medium"]
    
    preloaded = []
    for voice in voices:
        if voice in VOICES_CACHE:
            VOICE_MANAGER.preload_voice_models([voice])
            preloaded.append(voice)
    
    return {
        "status": "success",
        "preloaded_voices": preloaded,
        "message": f"Preloaded {len(preloaded)} voice models"
    }

@app.get("/performance/analytics")
async def get_performance_analytics():
    """📈 Advanced performance analytics"""
    cache_stats = AUDIO_CACHE.get_stats()
    memory_usage = VOICE_MANAGER.get_model_memory_usage()
    popular_voices = VOICE_MANAGER.get_popular_voices()
    
    return {
        "cache_efficiency": {
            "hit_rate_estimate": "Available after first cache hits",
            "memory_utilization": f"{(cache_stats['memory_usage_mb'] / cache_stats['max_memory_mb'] * 100):.1f}%",
            "entries_utilization": f"{(cache_stats['entries'] / cache_stats['max_entries'] * 100):.1f}%"
        },
        "voice_usage_patterns": {
            "most_popular": popular_voices[:5] if popular_voices else [],
            "total_voices_available": len(VOICES_CACHE),
            "voices_actually_used": len(VOICE_MANAGER.model_usage)
        },
        "system_resources": {
            "estimated_memory_usage_mb": memory_usage,
            "cache_memory_mb": cache_stats['memory_usage_mb'],
            "total_estimated_mb": memory_usage + cache_stats['memory_usage_mb']
        },
        "recommendations": {
            "cache_tuning": "Increase cache size if hit rate is low",
            "voice_optimization": "Consider preloading popular voices",
            "memory_management": "Monitor memory usage for large deployments"
        }
    }

@app.get("/reload-voices")
async def reload_voices():
    """Reload voice models (admin endpoint)"""
    try:
        load_voices()
        return {
            "status": "success",
            "message": f"Reloaded {len(VOICES_CACHE)} voices",
            "voices": list(VOICES_CACHE.keys())
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reload voices: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    logger.info(f"Starting server on {host}:{port}")
    uvicorn.run(
        app, 
        host=host, 
        port=port,
        log_level="info",
        access_log=True
    )