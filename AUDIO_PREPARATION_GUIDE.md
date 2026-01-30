# 🎵 Audio Preparation Guide

## How to Get Sample Audio for Testing

### Option 1: Use the Provided Sample
The organizers mentioned they will provide a Google Drive link with sample MP3 audio. Download that file.

### Option 2: Create Your Own Test Samples

#### For Human Voice Samples:
1. **Record yourself**: Use your phone's voice recorder
2. **Convert to MP3**: Use online tools like CloudConvert
3. **Or use free samples**: 
   - https://freesound.org (search for "speech")
   - Record a WhatsApp voice note and export

#### For AI Voice Samples:
1. **Generate AI voice**: Use free TTS services:
   - Google TTS: https://cloud.google.com/text-to-speech
   - ElevenLabs: https://elevenlabs.io (free tier)
   - Natural Readers: https://www.naturalreaders.com
   - TTSMaker: https://ttsmaker.com (free, no login)

2. **Generate in different languages**:
   - Tamil: Use Google TTS or AI4Bharat
   - Hindi: Use Google TTS
   - Telugu/Malayalam: Use Google TTS or ElevenLabs

---

## How to Convert Audio to Base64

### Method 1: Using Python (Recommended)

```python
import base64

# Read your MP3 file
with open('your_audio.mp3', 'rb') as audio_file:
    audio_bytes = audio_file.read()
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

# Save to a text file for easy copying
with open('audio_base64.txt', 'w') as f:
    f.write(audio_base64)

print("Base64 encoded audio saved to audio_base64.txt")
print(f"First 100 characters: {audio_base64[:100]}")
```

### Method 2: Using Command Line

#### On Linux/Mac:
```bash
base64 -i your_audio.mp3 -o audio_base64.txt
```

#### On Windows (PowerShell):
```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("your_audio.mp3")) | Out-File audio_base64.txt
```

### Method 3: Using Online Tools

1. Go to https://base64.guru/converter/encode/audio
2. Upload your MP3 file
3. Click "Encode"
4. Copy the base64 string

⚠️ **Warning**: Don't use online tools for sensitive audio!

---

## Testing Your API with the Base64 Audio

### Method 1: Using Python

```python
import requests
import base64
import json

# Encode audio
with open('sample.mp3', 'rb') as f:
    audio_base64 = base64.b64encode(f.read()).decode()

# Call API
response = requests.post(
    'https://your-app.onrender.com/detect-voice',
    headers={
        'X-API-Key': 'HCL_GUVI_2024_VOICE_DETECTION_KEY',
        'Content-Type': 'application/json'
    },
    json={'audio_base64': audio_base64}
)

print(json.dumps(response.json(), indent=2))
```

### Method 2: Using cURL

```bash
# First encode the audio
base64 -i sample.mp3 -o encoded.txt

# Then test (replace BASE64_STRING with content from encoded.txt)
curl -X POST "https://your-app.onrender.com/detect-voice" \
  -H "X-API-Key: HCL_GUVI_2024_VOICE_DETECTION_KEY" \
  -H "Content-Type: application/json" \
  -d '{"audio_base64": "BASE64_STRING_HERE"}'
```

### Method 3: Using Postman

1. Open Postman
2. Create a new POST request
3. URL: `https://your-app.onrender.com/detect-voice`
4. Headers:
   - `X-API-Key`: `HCL_GUVI_2024_VOICE_DETECTION_KEY`
   - `Content-Type`: `application/json`
5. Body (raw JSON):
```json
{
  "audio_base64": "PASTE_YOUR_BASE64_HERE"
}
```
6. Click "Send"

### Method 4: Using the Interactive Docs

1. Go to `https://your-app.onrender.com/docs`
2. Click on `/detect-voice` endpoint
3. Click "Try it out"
4. Fill in:
   - `X-API-Key`: `HCL_GUVI_2024_VOICE_DETECTION_KEY`
   - `audio_base64`: Your base64 string
5. Click "Execute"

---

## Sample Audio Recommendations

### Good Test Samples Should Have:
- Clear voice (minimal background noise)
- 3-10 seconds duration
- Single speaker
- MP3 format
- Sample rate: 16kHz - 44.1kHz

### Test Coverage:
Test your API with:
- ✅ Human voice (different ages, genders)
- ✅ AI-generated voice (different TTS engines)
- ✅ All 5 languages (Tamil, English, Hindi, Malayalam, Telugu)
- ✅ Different speaking styles (formal, casual)
- ✅ Different audio qualities

---

## Quick Test Script

Save this as `quick_test.py`:

```python
import requests
import base64
import sys

if len(sys.argv) < 2:
    print("Usage: python quick_test.py <audio_file.mp3>")
    sys.exit(1)

audio_file = sys.argv[1]
api_url = "https://your-app.onrender.com/detect-voice"
api_key = "HCL_GUVI_2024_VOICE_DETECTION_KEY"

# Encode audio
with open(audio_file, 'rb') as f:
    audio_b64 = base64.b64encode(f.read()).decode()

# Call API
response = requests.post(
    api_url,
    headers={'X-API-Key': api_key},
    json={'audio_base64': audio_b64}
)

# Display result
result = response.json()
print(f"\nFile: {audio_file}")
print(f"Classification: {result['classification']}")
print(f"Confidence: {result['confidence_score']:.1%}")
print(f"Explanation: {result['explanation']}\n")
```

Usage:
```bash
python quick_test.py sample_tamil.mp3
python quick_test.py sample_english.mp3
```

---

## Troubleshooting

### Issue: "Invalid base64 encoding"
**Fix**: Make sure you copied the entire base64 string without any extra spaces or newlines

### Issue: Audio file too large
**Fix**: 
- Keep audio under 5MB
- Use online compressor: https://www.freeconvert.com/audio-compressor
- Reduce bitrate to 64kbps or 128kbps

### Issue: Unsupported audio format
**Fix**: Convert to MP3 using:
- FFmpeg: `ffmpeg -i input.wav output.mp3`
- Online: https://cloudconvert.com/wav-to-mp3

---

## Free Resources for Test Audio

### Human Voice Samples:
- LibriVox: https://librivox.org (free audiobooks)
- Common Voice: https://commonvoice.mozilla.org
- VoxForge: http://www.voxforge.org

### AI Voice Generators (for testing):
- Google Cloud TTS: Free tier available
- Amazon Polly: Free tier available  
- TTSMaker: Free, unlimited
- Natural Readers: Free online
- ElevenLabs: Free tier

### Multi-language Samples:
- Tatoeba: https://tatoeba.org (sentences in many languages)
- CommonVoice: Has Tamil, Hindi, Telugu

---

## Best Practices

1. **Keep it simple**: Start with short, clear audio clips
2. **Test incrementally**: Test one language at a time
3. **Compare results**: Test both human and AI samples to verify accuracy
4. **Document**: Keep track of which samples gave which results
5. **Edge cases**: Test with different accents, speeds, quality levels

Good luck with testing! 🎤
