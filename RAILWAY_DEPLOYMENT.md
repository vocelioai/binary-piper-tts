# Railway Deployment Guide

## 🚀 Quick Deploy to Railway

Your Binary Piper TTS service is **ready for Railway deployment** with automatic voice downloading!

### What Railway Will Do Automatically:

✅ **Download ALL 73 voices** during build (takes ~5-10 minutes)  
✅ **Set UTC timezone** for global compatibility  
✅ **Configure health checks** with proper timeout  
✅ **Handle dynamic PORT** assignment  
✅ **Enable HTTPS** with custom domain  

### Deployment Steps:

1. **Connect Repository**
   - Go to [railway.app](https://railway.app)
   - Click "Deploy from GitHub repo"
   - Select `vocelioai/binary-piper-tts`

2. **Automatic Configuration**
   - Railway detects Dockerfile automatically
   - Build starts with voice model downloading
   - Service deploys on custom Railway domain

3. **Access Your TTS Service**
   - Web UI: `https://your-app.railway.app/`
   - API: `https://your-app.railway.app/api`
   - Health: `https://your-app.railway.app/health`

### Time Zone Support:

🌍 **Global Deployment Ready**
- UTC timezone set for universal compatibility
- Timestamps in ISO format with UTC
- Works across all time zones automatically

### Voice Model Download:

📦 **73 Voices Across 36 Languages**
- Arabic, Chinese, English, Spanish, German, French, Russian
- Italian, Portuguese, Dutch, Polish, Czech, Turkish
- And 24+ more languages
- Total download: ~2-3GB during build
- Cached permanently on Railway

### Expected Build Time:

⏱️ **Build Process:**
- System dependencies: ~2 minutes
- Voice model download: ~8-12 minutes  
- Total build time: ~15 minutes
- **Subsequent deploys**: ~2 minutes (cached)

### Railway Resource Requirements:

💾 **Recommended Plan:**
- **Memory**: 2GB+ (for 73 voice models)
- **CPU**: 1 vCPU minimum
- **Storage**: 4GB+ (voice models + OS)
- **Bandwidth**: As needed for TTS requests

### Custom Domain Setup:

🌐 **For Vocelio.ai Integration:**
```bash
# After deployment, add custom domain:
tts.vocelio.ai → your-railway-app.railway.app
```

### Environment Variables (Pre-configured):

```toml
TZ = "UTC"                    # Global timezone
PYTHONUNBUFFERED = "1"        # Better logging
MAX_TEXT_LENGTH = "1000"      # Request limits
LOG_LEVEL = "INFO"            # Production logging
```

### API Integration Example:

```javascript
// Perfect for Vocelio.ai call center
const response = await fetch('https://your-tts.railway.app/synthesize', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: 'Hello, this is your automated assistant.',
    voice: 'en_US-lessac-medium'
  })
});

const audioBlob = await response.blob();
// Use audio in your call center platform
```

### Health Monitoring:

🔍 **Built-in Health Checks:**
- Endpoint: `/health`
- Checks: Piper binary, voice models, file system
- Timeout: 300s (accommodates voice loading)
- Auto-restart on failure

### Cost Optimization:

💰 **Railway Pricing Tips:**
- Hobby plan: Good for testing/demo
- Pro plan: Recommended for production call center
- Usage-based billing scales with your TTS requests

### Support & Troubleshooting:

🛠️ **Common Issues:**
- **Long initial build**: Normal for voice downloading
- **Memory errors**: Upgrade to higher memory plan
- **Timeout on health check**: Increase timeout in Railway settings

---

## Ready to Deploy? 

1. **Fork/Push** this repo to your GitHub
2. **Connect** to Railway
3. **Deploy** automatically
4. **Access** your global TTS service in ~15 minutes!

Your service will be available worldwide with all voices pre-loaded! 🎉
