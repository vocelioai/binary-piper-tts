FROM python:3.11-slim

WORKDIR /app

# Install minimal dependencies
RUN apt-get update && \
    apt-get install -y wget curl && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir fastapi uvicorn aiofiles

# Copy app files
COPY . .

# Get Piper binary
RUN wget -q -O piper.tar.gz "https://github.com/rhasspy/piper/releases/latest/download/piper_linux_x86_64.tar.gz" && \
    tar -xzf piper.tar.gz && \
    mv piper/piper /usr/local/bin/piper && \
    chmod +x /usr/local/bin/piper && \
    rm -rf piper.tar.gz piper/

ENV PORT=8000
ENV PYTHONUNBUFFERED=1

EXPOSE $PORT

# Start with minimal models
CMD python download_models_minimal.py && exec uvicorn app:app --host 0.0.0.0 --port $PORT
