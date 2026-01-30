# 🚀 DEPLOYMENT GUIDE - Step by Step

## Easiest Method: Deploy to Render (FREE - Recommended)

### Step 1: Prepare Your Files
You already have all the files needed:
- `app.py` - Main application
- `requirements.txt` - Dependencies
- `Procfile` - Deployment configuration
- `README.md` - Documentation

### Step 2: Upload to GitHub (Optional but Recommended)

1. Create a new repository on GitHub
2. Upload all the files to the repository
3. Or use GitHub Desktop to push files

**Alternative**: You can deploy directly without GitHub (see Option B below)

### Step 3: Deploy to Render

#### Option A: Deploy from GitHub (Recommended)

1. Go to https://render.com and sign up (free)

2. Click "New +" button → Select "Web Service"

3. Connect your GitHub account and select the repository

4. Configure the service:
   - **Name**: `ai-voice-detection` (or your choice)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Select "Free"

5. Click "Create Web Service"

6. Wait 5-10 minutes for deployment

7. Your API will be available at: `https://ai-voice-detection-xxxx.onrender.com`

#### Option B: Deploy without GitHub

1. Go to https://render.com and sign up

2. Click "New +" → "Web Service"

3. Select "Build and deploy from a Git repository"

4. Choose "Public Git repository" and paste: Your repository URL
   OR
   Click "Deploy from URL" if you uploaded files somewhere

5. Follow the same configuration as Option A

### Step 4: Test Your Deployed API

```bash
# Test health endpoint
curl https://your-app-name.onrender.com/health

# Test voice detection (you'll need to provide base64 audio)
curl -X POST "https://your-app-name.onrender.com/detect-voice" \
  -H "X-API-Key: HCL_GUVI_2024_VOICE_DETECTION_KEY" \
  -H "Content-Type: application/json" \
  -d '{"audio_base64": "YOUR_BASE64_AUDIO"}'
```

### Step 5: Get Interactive Documentation

Visit: `https://your-app-name.onrender.com/docs`

This provides an interactive Swagger UI to test your API!

---

## Alternative: Deploy to Railway (FREE)

### Step 1: Sign Up
Go to https://railway.app and sign up with GitHub

### Step 2: Deploy

1. Click "New Project"

2. Select "Deploy from GitHub repo" (or use Railway CLI)

3. Select your repository

4. Railway auto-detects Python and installs dependencies

5. Your app will be deployed automatically!

6. Click "Settings" → "Generate Domain" to get your public URL

### Step 3: Test
Your API will be at: `https://your-app.railway.app`

---

## Alternative: Deploy to PythonAnywhere (FREE)

### Step 1: Sign Up
Go to https://www.pythonanywhere.com and create a free account

### Step 2: Upload Files

1. Go to "Files" tab
2. Upload all your files (app.py, requirements.txt, etc.)

### Step 3: Install Dependencies

1. Go to "Consoles" tab
2. Start a Bash console
3. Run:
```bash
pip install --user -r requirements.txt
```

### Step 4: Configure Web App

1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration" → Python 3.10
4. Configure WSGI file to point to your app
5. Click "Reload" to start the app

### Step 5: Access
Your API will be at: `https://yourusername.pythonanywhere.com`

---

## 📝 What to Submit for Buildathon

After deployment, submit:

1. **API Endpoint URL**: 
   `https://your-app-name.onrender.com/detect-voice`

2. **API Key**: 
   `HCL_GUVI_2024_VOICE_DETECTION_KEY`

3. **Documentation Link** (optional):
   `https://your-app-name.onrender.com/docs`

4. **Test Command**:
```bash
curl -X POST "https://your-app-name.onrender.com/detect-voice" \
  -H "X-API-Key: HCL_GUVI_2024_VOICE_DETECTION_KEY" \
  -H "Content-Type: application/json" \
  -d @test_audio.json
```

---

## 🧪 Testing Before Submission

### 1. Test with Sample Audio

Download a sample MP3, then:

```python
import base64

# Encode your audio
with open('sample.mp3', 'rb') as f:
    audio_b64 = base64.b64encode(f.read()).decode()
    print(audio_b64[:100])  # Print first 100 chars
```

### 2. Test the API

Use the encoded audio in your API request

### 3. Verify Response Format

Ensure response has:
- `classification` (AI_GENERATED or HUMAN)
- `confidence_score` (0.0 to 1.0)
- `explanation` (text)
- `processing_time_ms` (integer)

---

## ⚠️ Troubleshooting

### Issue: "Application Error" on Render
**Solution**: Check logs in Render dashboard. Usually it's a missing dependency.

### Issue: API returns 500 error
**Solution**: 
1. Check if audio is properly base64 encoded
2. Verify MP3 file is not corrupted
3. Check Render logs for specific error

### Issue: Slow response time
**Solution**: First request on free tier is slow (cold start). Subsequent requests are faster.

### Issue: API key not working
**Solution**: Make sure header is exactly `X-API-Key` (case-sensitive)

---

## 🎯 Quick Checklist

- ✅ All files uploaded to GitHub/deployment platform
- ✅ Render/Railway account created
- ✅ Web service deployed successfully
- ✅ Public URL obtained
- ✅ API tested with sample audio
- ✅ Health endpoint working (`/health`)
- ✅ Documentation accessible (`/docs`)
- ✅ Response format matches requirements
- ✅ API key authentication working
- ✅ Multi-language support verified (test with different language samples)

---

## 🔗 Important Links

- **Render**: https://render.com
- **Railway**: https://railway.app
- **PythonAnywhere**: https://www.pythonanywhere.com
- **API Testing Tool**: https://reqbin.com or Postman

---

## 💡 Pro Tips

1. **Test locally first**: Run `python app.py` and test on `localhost:8000` before deploying

2. **Use the /docs endpoint**: It provides interactive API testing

3. **Monitor logs**: Check deployment platform logs if something goes wrong

4. **Free tier limitations**: 
   - Render: App sleeps after 15 min of inactivity (wakes up on request)
   - Railway: 500 hours/month free
   - PythonAnywhere: Limited CPU time

5. **Keep API key secret**: Change it before production use!

---

## Need Help?

If you face any issues:
1. Check the logs on your deployment platform
2. Test locally first to isolate the issue
3. Verify all dependencies are in requirements.txt
4. Check that file paths are correct

Good luck with your buildathon! 🚀
