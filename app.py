import os
import io
import tempfile
import subprocess
import json
import asyncio
from datetime import datetime, timezone
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

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

MAX_TEXT_LENGTH = 1000

logger.info(f"Resolved MODELS_DIR={MODELS_DIR}")
logger.info(f"Resolved PIPER_BINARY={PIPER_BINARY}")

# Request models
class SynthesisRequest(BaseModel):
    text: str
    voice: str = "en_US-lessac-medium"
    speaker_id: Optional[int] = 0

class VoiceInfo(BaseModel):
    name: str
    language: str
    sample_rate: int
    num_speakers: int
    model_path: str
    config_path: str

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

def validate_text_input(text: str) -> str:
    """Validate and sanitize text input"""
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    text = text.strip()
    if len(text) > MAX_TEXT_LENGTH:
        raise HTTPException(
            status_code=400, 
            detail=f"Text too long. Maximum {MAX_TEXT_LENGTH} characters allowed"
        )
    
    return text

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
        "endpoints": {
            "voices": "/voices",
            "synthesize": "/synthesize",
            "health": "/health",
            "web_ui": "/",
            "api_info": "/api"
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

@app.post("/synthesize")
async def synthesize_speech(request: SynthesisRequest):
    """Synthesize speech using Piper binary"""
    
    # Validate inputs
    text = validate_text_input(request.text)
    voice_info = validate_voice_id(request.voice)
    
    # Validate speaker ID
    if request.speaker_id and request.speaker_id >= voice_info.num_speakers:
        raise HTTPException(
            status_code=400,
            detail=f"Speaker ID {request.speaker_id} not available. Voice has {voice_info.num_speakers} speakers (0-{voice_info.num_speakers-1})"
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
        
        logger.info(f"Synthesizing: '{text[:50]}...' with voice '{request.voice}'")
        
        # Run Piper binary
        result = subprocess.run(
            cmd,
            input=text,
            text=True,
            capture_output=True,
            timeout=30,
            check=False
        )
        
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
        
        logger.info(f"Successfully synthesized {len(audio_data)} bytes of audio")
        
        # Return audio as streaming response
        return StreamingResponse(
            io.BytesIO(audio_data),
            media_type="audio/wav",
            headers={
                "Content-Disposition": f"attachment; filename=speech_{request.voice}.wav",
                "Content-Length": str(len(audio_data)),
                "X-Voice-Used": request.voice,
                "X-Speaker-ID": str(request.speaker_id or 0),
                "X-Text-Length": str(len(text))
            }
        )
        
    except subprocess.TimeoutExpired:
        logger.error("Piper synthesis timeout")
        raise HTTPException(status_code=504, detail="Synthesis timeout (30s limit)")
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