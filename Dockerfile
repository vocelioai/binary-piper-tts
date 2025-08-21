FROM python:3.11-slim

WORKDIR /app

# Install dependencies including espeak-ng for Piper
RUN apt-get update && \
    apt-get install -y wget curl espeak-ng espeak-ng-data && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir fastapi uvicorn aiofiles

# Copy app files
COPY . .

# Get Piper binary and libraries
RUN wget -q -O piper.tar.gz "https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz" && \
    tar -xzf piper.tar.gz && \
    cp piper/piper /usr/local/bin/ && \
    cp piper/lib/* /usr/local/lib/ && \
    ldconfig && \
    chmod +x /usr/local/bin/piper && \
    rm -rf piper.tar.gz piper/

ENV PORT=8000
ENV PYTHONUNBUFFERED=1

EXPOSE $PORT

# Start with minimal models
CMD python download_models_minimal.py && exec uvicorn app:app --host 0.0.0.0 --port $PORT
