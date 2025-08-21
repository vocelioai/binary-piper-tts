FROM python:3.11-slim

WORKDIR /app

# Install dependencies including espeak-ng for Piper
RUN apt-get update && \
    apt-get install -y wget curl espeak-ng espeak-ng-data && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir fastapi uvicorn aiofiles

# Copy app files
COPY . .

# Get Piper binary and libraries - use complete installation
RUN wget -q -O piper.tar.gz "https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz" && \
    tar -xzf piper.tar.gz && \
    mkdir -p /opt/piper && \
    cp -r piper/* /opt/piper/ && \
    ln -s /opt/piper/piper /usr/local/bin/piper && \
    chmod +x /opt/piper/piper && \
    echo "/opt/piper/lib" > /etc/ld.so.conf.d/piper.conf && \
    ldconfig && \
    rm -rf piper.tar.gz piper/

ENV PORT=8000
ENV PYTHONUNBUFFERED=1
ENV LD_LIBRARY_PATH=/opt/piper/lib:$LD_LIBRARY_PATH

EXPOSE $PORT

# Start with enhanced download for 50+ voices within time limits
CMD python download_models_enhanced.py && exec uvicorn app:app --host 0.0.0.0 --port $PORT
