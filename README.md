AI Voice Detection API - HCL GUVI Buildathon

Multi-language AI voice detection system that determines whether a voice sample is AI-generated or human-generated.

Features

-  Supports 5 languages: Tamil, English, Hindi, Malayalam, Telugu
-  Base64-encoded MP3 input
- JSON response with classification, confidence, and explanation
- API key authentication
- Language-agnostic audio feature analysis
- REST API with FastAPI

API Specification

Endpoint
```
POST /detect-voice
```

Headers
```
X-API-Key: HCL_GUVI_2024_VOICE_DETECTION_KEY
Content-Type: application/json
```

Request Body
```json
{
  "audio_base64": "BASE64_ENCODED_MP3_AUDIO"
}
```

Response
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
- Too consistent spectral characteristics
- Unnaturally smooth pitch contour
- Highly consistent energy levels
- Controlled spectral bandwidth
- Lack of natural noise/breathing patterns

### Key Human Voice Indicators:
- Natural spectral variation
- Natural pitch fluctuations
- Energy variation (breathing, pauses)
- Natural noise patterns
- Formant pattern variation

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

the `/docs` endpoint for interactive API documentation.
