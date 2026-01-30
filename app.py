from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import io
import numpy as np
import librosa
import soundfile as sf
from typing import Optional
import time
import hashlib

app = FastAPI(
    title="AI Voice Detection API",
    description="Detects whether a voice sample is AI-generated or human across multiple languages",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key (you should change this!)
VALID_API_KEY = "HCL_GUVI_2024_VOICE_DETECTION_KEY"

class VoiceDetectionRequest(BaseModel):
    audio_base64: str
    
class VoiceDetectionResponse(BaseModel):
    classification: str
    confidence_score: float
    explanation: str
    language_detected: Optional[str] = None
    processing_time_ms: int

def verify_api_key(x_api_key: str = Header(...)):
    """Verify API key from headers"""
    if x_api_key != VALID_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

def extract_audio_features(audio_data, sr):
    """
    Extract comprehensive audio features for AI vs Human detection
    """
    features = {}
    
    # 1. MFCC (Mel-frequency cepstral coefficients) - captures spectral envelope
    mfcc = librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=20)
    features['mfcc_mean'] = np.mean(mfcc, axis=1)
    features['mfcc_std'] = np.std(mfcc, axis=1)
    features['mfcc_var'] = np.var(mfcc, axis=1)
    
    # 2. Spectral features
    spectral_centroids = librosa.feature.spectral_centroid(y=audio_data, sr=sr)[0]
    features['spectral_centroid_mean'] = np.mean(spectral_centroids)
    features['spectral_centroid_std'] = np.std(spectral_centroids)
    
    spectral_rolloff = librosa.feature.spectral_rolloff(y=audio_data, sr=sr)[0]
    features['spectral_rolloff_mean'] = np.mean(spectral_rolloff)
    features['spectral_rolloff_std'] = np.std(spectral_rolloff)
    
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=audio_data, sr=sr)[0]
    features['spectral_bandwidth_mean'] = np.mean(spectral_bandwidth)
    features['spectral_bandwidth_std'] = np.std(spectral_bandwidth)
    
    # 3. Zero Crossing Rate (indicates noisiness)
    zcr = librosa.feature.zero_crossing_rate(audio_data)[0]
    features['zcr_mean'] = np.mean(zcr)
    features['zcr_std'] = np.std(zcr)
    
    # 4. Chroma features (pitch class profiles)
    chroma = librosa.feature.chroma_stft(y=audio_data, sr=sr)
    features['chroma_mean'] = np.mean(chroma)
    features['chroma_std'] = np.std(chroma)
    
    # 5. RMS Energy
    rms = librosa.feature.rms(y=audio_data)[0]
    features['rms_mean'] = np.mean(rms)
    features['rms_std'] = np.std(rms)
    
    # 6. Pitch and fundamental frequency variations
    try:
        pitches, magnitudes = librosa.piptrack(y=audio_data, sr=sr)
        pitch_values = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            if pitch > 0:
                pitch_values.append(pitch)
        
        if len(pitch_values) > 0:
            features['pitch_mean'] = np.mean(pitch_values)
            features['pitch_std'] = np.std(pitch_values)
            features['pitch_range'] = np.max(pitch_values) - np.min(pitch_values)
        else:
            features['pitch_mean'] = 0
            features['pitch_std'] = 0
            features['pitch_range'] = 0
    except:
        features['pitch_mean'] = 0
        features['pitch_std'] = 0
        features['pitch_range'] = 0
    
    # 7. Tempo and rhythm
    tempo, beats = librosa.beat.beat_track(y=audio_data, sr=sr)
    features['tempo'] = tempo
    
    return features

def detect_ai_voice(features):
    """
    AI Voice Detection Algorithm based on audio features
    
    Key indicators:
    - AI voices tend to have more consistent spectral features (lower std dev)
    - AI voices have smoother pitch variations
    - AI voices lack natural breathing artifacts
    - AI voices have very consistent energy levels
    """
    
    ai_score = 0.0
    human_score = 0.0
    indicators = []
    
    # 1. Spectral Consistency Check
    # AI voices are typically TOO consistent
    spectral_consistency = features['spectral_centroid_std'] / (features['spectral_centroid_mean'] + 1e-6)
    if spectral_consistency < 0.15:  # Very consistent = likely AI
        ai_score += 0.20
        indicators.append("Very consistent spectral characteristics")
    elif spectral_consistency > 0.35:  # More variation = likely human
        human_score += 0.15
        indicators.append("Natural spectral variation")
    
    # 2. MFCC Variance Analysis
    # Human voices have more natural variation in formants
    mfcc_variance_avg = np.mean(features['mfcc_var'])
    if mfcc_variance_avg < 50:  # Low variance = AI
        ai_score += 0.18
        indicators.append("Low formant variation")
    elif mfcc_variance_avg > 150:  # Higher variance = human
        human_score += 0.15
        indicators.append("Natural formant patterns")
    
    # 3. Pitch Variation Analysis
    # AI voices have unnaturally smooth pitch
    if features['pitch_std'] > 0:
        pitch_variation_coefficient = features['pitch_std'] / (features['pitch_mean'] + 1e-6)
        if pitch_variation_coefficient < 0.08:  # Too smooth = AI
            ai_score += 0.22
            indicators.append("Unnaturally smooth pitch contour")
        elif pitch_variation_coefficient > 0.20:  # More variation = human
            human_score += 0.18
            indicators.append("Natural pitch fluctuations")
    
    # 4. Energy Consistency
    # AI voices maintain very consistent energy
    energy_consistency = features['rms_std'] / (features['rms_mean'] + 1e-6)
    if energy_consistency < 0.25:  # Too consistent = AI
        ai_score += 0.15
        indicators.append("Highly consistent energy levels")
    elif energy_consistency > 0.50:  # More variation = human
        human_score += 0.12
        indicators.append("Natural energy variation")
    
    # 5. Zero Crossing Rate Pattern
    # AI voices often have different noise characteristics
    zcr_ratio = features['zcr_std'] / (features['zcr_mean'] + 1e-6)
    if zcr_ratio < 0.30:  # Low = potentially AI
        ai_score += 0.12
        indicators.append("Artificial noise profile")
    elif zcr_ratio > 0.65:  # Higher = human breathing, natural noise
        human_score += 0.15
        indicators.append("Natural noise patterns")
    
    # 6. Spectral Bandwidth Analysis
    # AI tends to have narrower, more controlled bandwidth
    bandwidth_coefficient = features['spectral_bandwidth_std'] / (features['spectral_bandwidth_mean'] + 1e-6)
    if bandwidth_coefficient < 0.20:  # Narrow = AI
        ai_score += 0.13
        indicators.append("Controlled spectral bandwidth")
    elif bandwidth_coefficient > 0.45:  # Wider = human
        human_score += 0.12
        indicators.append("Natural bandwidth variation")
    
    # Calculate final confidence
    total_score = ai_score + human_score
    if total_score > 0:
        ai_confidence = ai_score / total_score
        human_confidence = human_score / total_score
    else:
        # Default to slight human bias if unclear
        ai_confidence = 0.45
        human_confidence = 0.55
    
    # Determine classification
    if ai_confidence > human_confidence:
        classification = "AI_GENERATED"
        confidence = ai_confidence
    else:
        classification = "HUMAN"
        confidence = human_confidence
    
    # Build explanation
    if len(indicators) > 0:
        explanation = "Analysis detected: " + "; ".join(indicators[:3])
    else:
        explanation = "Inconclusive audio features, defaulting to human classification"
    
    return classification, confidence, explanation

@app.get("/")
async def root():
    return {
        "message": "AI Voice Detection API",
        "status": "online",
        "supported_languages": ["Tamil", "English", "Hindi", "Malayalam", "Telugu"],
        "endpoints": {
            "detection": "/detect-voice (POST)",
            "health": "/health (GET)"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": time.time()}

@app.post("/detect-voice", response_model=VoiceDetectionResponse)
async def detect_voice(request: VoiceDetectionRequest, api_key: str = Header(..., alias="X-API-Key")):
    """
    Detect whether a voice sample is AI-generated or human
    
    Headers:
    - X-API-Key: Your API key
    
    Body:
    - audio_base64: Base64-encoded MP3 audio file
    
    Returns:
    - classification: "AI_GENERATED" or "HUMAN"
    - confidence_score: 0.0 to 1.0
    - explanation: Reasoning behind the classification
    - language_detected: Detected language (optional)
    - processing_time_ms: Processing time in milliseconds
    """
    start_time = time.time()
    
    # Verify API key
    verify_api_key(api_key)
    
    try:
        # Decode base64 audio
        audio_bytes = base64.b64decode(request.audio_base64)
        
        # Load audio using soundfile and librosa
        audio_buffer = io.BytesIO(audio_bytes)
        audio_data, sample_rate = sf.read(audio_buffer)
        
        # Convert to mono if stereo
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)
        
        # Resample to standard rate if needed
        if sample_rate != 22050:
            audio_data = librosa.resample(audio_data, orig_sr=sample_rate, target_sr=22050)
            sample_rate = 22050
        
        # Extract features
        features = extract_audio_features(audio_data, sample_rate)
        
        # Detect AI vs Human
        classification, confidence, explanation = detect_ai_voice(features)
        
        # Calculate processing time
        processing_time = int((time.time() - start_time) * 1000)
        
        return VoiceDetectionResponse(
            classification=classification,
            confidence_score=round(confidence, 3),
            explanation=explanation,
            language_detected=None,  # Language detection can be added if needed
            processing_time_ms=processing_time
        )
        
    except base64.binascii.Error:
        raise HTTPException(status_code=400, detail="Invalid base64 encoding")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
