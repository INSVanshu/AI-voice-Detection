"""
Example script showing how to use the AI Voice Detection API
"""

import requests
import base64
import json

def detect_voice_from_file(audio_file_path, api_url, api_key):
    """
    Detect if a voice in an audio file is AI-generated or human
    
    Args:
        audio_file_path: Path to MP3 audio file
        api_url: API endpoint URL (e.g., https://your-app.onrender.com/detect-voice)
        api_key: Your API key
    
    Returns:
        dict: API response with classification and confidence
    """
    
    # Read and encode the audio file to base64
    with open(audio_file_path, 'rb') as audio_file:
        audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    
    # Prepare the request
    headers = {
        'X-API-Key': api_key,
        'Content-Type': 'application/json'
    }
    
    payload = {
        'audio_base64': audio_base64
    }
    
    # Send POST request
    response = requests.post(api_url, json=payload, headers=headers)
    
    # Check if request was successful
    if response.status_code == 200:
        return response.json()
    else:
        return {
            'error': f'Request failed with status code {response.status_code}',
            'details': response.text
        }

# Example usage
if __name__ == '__main__':
    # Configuration
    API_URL = "https://your-app-name.onrender.com/detect-voice"  # Replace with your actual URL
    API_KEY = "HCL_GUVI_2024_VOICE_DETECTION_KEY"
    AUDIO_FILE = "sample_audio.mp3"  # Replace with your audio file
    
    print("🎤 AI Voice Detection API - Example Usage\n")
    print(f"Testing with audio file: {AUDIO_FILE}")
    print(f"API Endpoint: {API_URL}\n")
    
    try:
        # Detect voice
        result = detect_voice_from_file(AUDIO_FILE, API_URL, API_KEY)
        
        # Display results
        print("="*60)
        print("RESULTS")
        print("="*60)
        print(json.dumps(result, indent=2))
        print("="*60)
        
        # Interpret results
        if 'classification' in result:
            classification = result['classification']
            confidence = result['confidence_score']
            explanation = result['explanation']
            
            print(f"\n📊 Classification: {classification}")
            print(f"🎯 Confidence: {confidence:.1%}")
            print(f"💡 Explanation: {explanation}")
            
            if classification == "AI_GENERATED":
                print("\n⚠️  This voice appears to be AI-generated")
            else:
                print("\n✅ This voice appears to be human")
        
    except FileNotFoundError:
        print(f"❌ Error: Audio file '{AUDIO_FILE}' not found!")
        print("Please provide a valid MP3 file path")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


# Example for batch processing multiple files
def batch_detect_voices(audio_files, api_url, api_key):
    """
    Process multiple audio files
    """
    results = {}
    
    for audio_file in audio_files:
        print(f"Processing {audio_file}...")
        result = detect_voice_from_file(audio_file, api_url, api_key)
        results[audio_file] = result
    
    return results


# Example for testing all 5 languages
def test_multilingual():
    """
    Example showing how to test with different language samples
    """
    API_URL = "https://your-app-name.onrender.com/detect-voice"
    API_KEY = "HCL_GUVI_2024_VOICE_DETECTION_KEY"
    
    language_samples = {
        'Tamil': 'sample_tamil.mp3',
        'English': 'sample_english.mp3',
        'Hindi': 'sample_hindi.mp3',
        'Malayalam': 'sample_malayalam.mp3',
        'Telugu': 'sample_telugu.mp3'
    }
    
    print("🌍 Testing Multi-Language Support\n")
    
    for language, audio_file in language_samples.items():
        try:
            result = detect_voice_from_file(audio_file, API_URL, API_KEY)
            classification = result.get('classification', 'UNKNOWN')
            confidence = result.get('confidence_score', 0)
            
            print(f"{language:12} - {classification:14} (Confidence: {confidence:.1%})")
        except FileNotFoundError:
            print(f"{language:12} - Sample file not found")
        except Exception as e:
            print(f"{language:12} - Error: {str(e)}")
