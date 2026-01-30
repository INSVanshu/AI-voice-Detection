# AI Voice Detection API - HCL GUVI Buildathon

Multi-language AI voice detection system that determines whether a voice sample is AI-generated or human-generated.

## Features

- ✅ Supports 5 languages: Tamil, English, Hindi, Malayalam, Telugu
- ✅ Base64-encoded MP3 input
- ✅ JSON response with classification, confidence, and explanation
- ✅ API key authentication
- ✅ Language-agnostic audio feature analysis
- ✅ REST API with FastAPI

## API Specification

### Endpoint
```
POST /detect-voice
```

### Headers
```
X-API-Key: HCL_GUVI_2024_VOICE_DETECTION_KEY
Content-Type: application/json
```

### Request Body
```json
{
  "audio_base64": "BASE64_ENCODED_MP3_AUDIO"
}
```

### Response
```json
{
  "classification": "AI_GENERATED" or "HUMAN",
  "confidence_score": 0.85,
  "explanation": "Analysis detected: Very consistent spectral characteristics; Low formant variation; Unnaturally smooth pitch contour",
  "language_detected": null,
  "processing_time_ms": 234
}
```

## Detection Method

The system analyzes multiple audio features:

1. **MFCC (Mel-frequency cepstral coefficients)** - Spectral envelope analysis
2. **Spectral Features** - Centroid, rolloff, bandwidth consistency
3. **Pitch Variation** - AI voices have unnaturally smooth pitch
4. **Energy Consistency** - AI maintains too-consistent energy levels
5. **Zero Crossing Rate** - Noise pattern analysis
6. **Formant Patterns** - Natural vs artificial voice characteristics

### Key AI Voice Indicators:
- ❌ Too consistent spectral characteristics
- ❌ Unnaturally smooth pitch contour
- ❌ Highly consistent energy levels
- ❌ Controlled spectral bandwidth
- ❌ Lack of natural noise/breathing patterns

### Key Human Voice Indicators:
- ✅ Natural spectral variation
- ✅ Natural pitch fluctuations
- ✅ Energy variation (breathing, pauses)
- ✅ Natural noise patterns
- ✅ Formant pattern variation

## Quick Start - Local Testing

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Server
```bash
python app.py
```

The server will start at `http://localhost:8000`

### 3. Test the API
```bash
# Visit the interactive docs
http://localhost:8000/docs

# Or use the test script
python test_api.py
```

## Deployment Instructions

### Option 1: Deploy to Render (Recommended - FREE)

1. **Create a Render account** at https://render.com

2. **Create a new Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository (or use "Deploy from URL")
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`

3. **Environment Variables** (Optional):
   - Add `API_KEY` if you want to customize it

4. **Deploy**: Click "Create Web Service"

5. **Get your URL**: Render will provide a URL like `https://your-app-name.onrender.com`

### Option 2: Deploy to Railway

1. **Create Railway account** at https://railway.app

2. **Deploy**:
   - Click "New Project" → "Deploy from GitHub repo"
   - Or use Railway CLI: `railway up`

3. **Configure**:
   - Railway auto-detects Python and installs requirements
   - Add domain in settings

4. **Get URL**: Railway provides URL like `https://your-app.railway.app`

### Option 3: Deploy to Python Anywhere

1. Sign up at https://www.pythonanywhere.com

2. Upload files via web interface

3. Configure web app with WSGI

### Option 4: Deploy to Heroku

1. Install Heroku CLI

2. Create `Procfile`:
```
web: uvicorn app:app --host 0.0.0.0 --port $PORT
```

3. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

## Testing Your Deployed API

### Using cURL:
```bash
# First, encode your audio file
base64 -i sample.mp3 -o encoded.txt

# Then test the API
curl -X POST "https://your-api-url.com/detect-voice" \
  -H "X-API-Key: HCL_GUVI_2024_VOICE_DETECTION_KEY" \
  -H "Content-Type: application/json" \
  -d '{"audio_base64": "PASTE_BASE64_HERE"}'
```

### Using Python:
```python
import requests
import base64

# Encode audio
with open("audio.mp3", "rb") as f:
    audio_base64 = base64.b64encode(f.read()).decode()

# Call API
response = requests.post(
    "https://your-api-url.com/detect-voice",
    headers={"X-API-Key": "HCL_GUVI_2024_VOICE_DETECTION_KEY"},
    json={"audio_base64": audio_base64}
)

print(response.json())
```

### Using Postman:
1. Create POST request to `https://your-api-url.com/detect-voice`
2. Add header: `X-API-Key: HCL_GUVI_2024_VOICE_DETECTION_KEY`
3. Body (raw JSON):
```json
{
  "audio_base64": "YOUR_BASE64_ENCODED_AUDIO"
}
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/detect-voice` | POST | Voice detection |
| `/docs` | GET | Interactive API documentation |

## Important Notes

1. **API Key**: Default is `HCL_GUVI_2024_VOICE_DETECTION_KEY` - change this in production!

2. **Audio Format**: Accepts Base64-encoded MP3 files

3. **Language Support**: Works across all 5 languages (Tamil, English, Hindi, Malayalam, Telugu) without language-specific processing

4. **No Hardcoding**: Uses real audio feature analysis, not hardcoded responses

5. **Scalability**: Can handle multiple concurrent requests

## Troubleshooting

### Error: "Invalid base64 encoding"
- Ensure audio is properly base64 encoded
- Check for extra whitespace or newlines

### Error: "Invalid API Key"
- Verify X-API-Key header is set correctly
- Check for typos in the key

### Error: "Error processing audio"
- Ensure file is a valid MP3
- Check file isn't corrupted
- Verify base64 encoding is complete

## Submission Checklist

- ✅ Publicly accessible API endpoint URL
- ✅ API key for authentication
- ✅ Supports all 5 languages
- ✅ Returns proper JSON format
- ✅ No hardcoding - uses actual ML/analysis
- ✅ Handles errors gracefully
- ✅ Includes confidence scores
- ✅ Provides explanations

## Example Submission Format

**API Endpoint:** `https://your-app-name.onrender.com/detect-voice`

**API Key:** `HCL_GUVI_2024_VOICE_DETECTION_KEY`

**Test Command:**
```bash
curl -X POST "https://your-app-name.onrender.com/detect-voice" \
  -H "X-API-Key: HCL_GUVI_2024_VOICE_DETECTION_KEY" \
  -H "Content-Type: application/json" \
  -d @request.json
```

## Architecture

```
Request → FastAPI → Base64 Decode → Audio Load (librosa/soundfile)
          ↓
Feature Extraction (MFCC, Spectral, Pitch, Energy)
          ↓
AI Detection Algorithm (Multi-feature analysis)
          ↓
Classification + Confidence Score + Explanation
          ↓
JSON Response
```

## License

Built for HCL GUVI Buildathon 2024

## Support

For issues or questions, check the `/docs` endpoint for interactive API documentation.
