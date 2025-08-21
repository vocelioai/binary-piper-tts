FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TZ=UTC

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    espeak-ng \
    espeak-ng-data \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make models directory
RUN mkdir -p models

# Download Piper binary and models during build
RUN wget -O piper.tar.gz "https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz" && \
    tar -xzf piper.tar.gz && \
    mv piper/piper /usr/local/bin/ && \
    chmod +x /usr/local/bin/piper && \
    rm -rf piper.tar.gz piper/ && \
    python download_models.py

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=60s --timeout=30s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start the application
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
