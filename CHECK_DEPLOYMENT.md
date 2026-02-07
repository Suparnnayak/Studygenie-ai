# Deployment Troubleshooting Guide

## 502 Bad Gateway - Common Causes & Fixes

### 1. Check Render Logs
Go to your Render dashboard → Your Service → Logs tab
Look for:
- Import errors
- Missing environment variables
- Application crashes

### 2. Verify Environment Variables in Render
In Render dashboard → Environment:
- ✅ `GEMINI_API_KEY` - MUST be set (get from https://makersuite.google.com/app/apikey)
- ✅ `SECRET_KEY` - Should be auto-generated or set manually
- ✅ `CORS_ORIGINS` - Set to `*` or your frontend URL
- ✅ `FLASK_DEBUG` - Set to `False` for production

### 3. Check Service Status
- Health endpoint: `https://studygenie-ai.onrender.com/health`
- If health works but upload doesn't → Service might be sleeping (free tier)
- If health doesn't work → App crashed on startup

### 4. Common Issues

**Issue: Missing GEMINI_API_KEY**
- Error in logs: "GEMINI_API_KEY not found"
- Fix: Add it in Render dashboard → Environment

**Issue: Import Errors**
- Check logs for Python import errors
- Fix: Ensure all dependencies in requirements.txt

**Issue: Service Sleeping (Free Tier)**
- First request takes 30-60 seconds
- Fix: Wait for wake-up or upgrade to paid plan

**Issue: Timeout**
- Processing takes too long
- Fix: Already set timeout to 120 seconds in gunicorn

### 5. Test Commands

```bash
# Test health (should work immediately)
curl https://studygenie-ai.onrender.com/health

# Test upload (may take 30-60s on first request)
curl -X POST https://studygenie-ai.onrender.com/api/upload-pdf \
  -F "file=@test.pdf"
```

### 6. Manual Restart
In Render dashboard:
- Click "Manual Deploy" → "Clear build cache & deploy"

### 7. Check Build Logs
Look for:
- ✅ "Build successful"
- ✅ "Starting service"
- ❌ Any red error messages

