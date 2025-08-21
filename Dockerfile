FROM ubuntu:22.04

WORKDIR /app

# Set timezone to UTC (optimal for global deployment)
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    python3.11 \
    python3.11-pip \
    python3.11-venv \
    espeak-ng \
    espeak-ng-data \
    libespeak-ng-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create symlinks for python
RUN ln -s /usr/bin/python3.11 /usr/bin/python3
RUN ln -s /usr/bin/python3.11 /usr/bin/python

# Download and install Piper binary
RUN echo "Downloading Piper TTS binary..." && \
    wget -O piper.tar.gz "https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz" && \
    tar -xzf piper.tar.gz && \
    mv piper/piper /usr/local/bin/ && \
    chmod +x /usr/local/bin/piper && \
    rm -rf piper.tar.gz piper/ && \
    echo "Piper binary installed successfully"

# Install Python dependencies
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Create models directory
RUN mkdir -p /app/models

# Copy application files
COPY . .

# Download voice models during build (all 73 voices across 36 languages)
RUN echo "Downloading all voice models for global deployment..." && \
    python3 download_models.py

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run on Railway's dynamic port or fallback to 8000
CMD ["sh", "-c", "python3 -m uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}"]
