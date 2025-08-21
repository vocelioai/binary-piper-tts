#!/usr/bin/env python3
"""
Flexible Voice Deployment Configuration
Choose your voice set based on deployment needs
"""
import os
import sys

# Deployment configurations
DEPLOYMENT_CONFIGS = {
    "minimal": {
        "script": "download_models_minimal.py",
        "voices": 5,
        "time": "~2 minutes",
        "description": "Essential voices: EN, ES, FR, DE, EN-GB",
        "use_case": "Quick testing, MVP deployment"
    },
    
    "progressive": {
        "script": "download_models_progressive.py", 
        "voices": "15-25",
        "time": "~5-8 minutes",
        "description": "Smart progressive download with time management",
        "use_case": "Current production setup, balanced approach"
    },
    
    "maximum": {
        "script": "download_models_maximum.py",
        "voices": "50-73", 
        "time": "~10-15 minutes",
        "description": "Complete voice catalog, all regions",
        "use_case": "Full global deployment, maximum language coverage"
    },
    
    "regional": {
        "script": "download_models_regional.py",
        "voices": "20-30",
        "time": "~6-10 minutes", 
        "description": "Focus on specific regions (Europe, Asia, etc.)",
        "use_case": "Targeted market deployment"
    }
}

def show_configs():
    """Display available deployment configurations"""
    print("🚀 Binary Piper TTS - Deployment Configurations\n")
    
    for config_name, config in DEPLOYMENT_CONFIGS.items():
        print(f"📦 {config_name.upper()}")
        print(f"   Voices: {config['voices']}")
        print(f"   Time: {config['time']}")
        print(f"   Description: {config['description']}")
        print(f"   Use Case: {config['use_case']}")
        print()

def update_deployment_files(config_name):
    """Update Dockerfile and Procfile to use selected configuration"""
    if config_name not in DEPLOYMENT_CONFIGS:
        print(f"❌ Unknown configuration: {config_name}")
        return False
    
    config = DEPLOYMENT_CONFIGS[config_name]
    script = config["script"]
    
    # Update Dockerfile
    dockerfile_content = f'''FROM python:3.11-slim

WORKDIR /app

# Install dependencies including espeak-ng for Piper
RUN apt-get update && \\
    apt-get install -y wget curl espeak-ng espeak-ng-data && \\
    rm -rf /var/lib/apt/lists/* && \\
    pip install --no-cache-dir fastapi uvicorn aiofiles

# Copy app files
COPY . .

# Get Piper binary and libraries - use complete installation
RUN wget -q -O piper.tar.gz "https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz" && \\
    tar -xzf piper.tar.gz && \\
    mkdir -p /opt/piper && \\
    cp -r piper/* /opt/piper/ && \\
    ln -s /opt/piper/piper /usr/local/bin/piper && \\
    chmod +x /opt/piper/piper && \\
    echo "/opt/piper/lib" > /etc/ld.so.conf.d/piper.conf && \\
    ldconfig && \\
    rm -rf piper.tar.gz piper/

ENV PORT=8000
ENV PYTHONUNBUFFERED=1
ENV LD_LIBRARY_PATH=/opt/piper/lib:$LD_LIBRARY_PATH

EXPOSE $PORT

# Use selected deployment configuration
CMD python {script} && exec uvicorn app:app --host 0.0.0.0 --port $PORT'''

    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    
    # Update Procfile
    procfile_content = f"web: python {script} && python -m uvicorn app:app --host 0.0.0.0 --port $PORT"
    
    with open("Procfile", "w") as f:
        f.write(procfile_content)
    
    print(f"✅ Updated deployment files for {config_name.upper()} configuration")
    print(f"   Script: {script}")
    print(f"   Expected voices: {config['voices']}")
    print(f"   Expected time: {config['time']}")
    
    return True

def main():
    """Main configuration interface"""
    if len(sys.argv) != 2:
        print("Usage: python configure_deployment.py <config_name>")
        print("Available configurations:")
        show_configs()
        return
    
    config_name = sys.argv[1].lower()
    
    if config_name == "list":
        show_configs()
        return
    
    if update_deployment_files(config_name):
        print(f"\\n🚀 Ready to deploy {config_name.upper()} configuration!")
        print("   Next steps:")
        print("   1. git add .")
        print("   2. git commit -m 'Update to {config_name} voice deployment'")
        print("   3. git push origin main")
        print("   4. Wait for Railway to redeploy")

if __name__ == "__main__":
    main()
