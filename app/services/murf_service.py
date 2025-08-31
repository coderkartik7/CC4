import requests
import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class MurfService:
    def __init__(self):
        self.api_key = os.getenv("MURF_API_KEY")
        self.base_url = "https://api.murf.ai/v1"
        self.headers = {
            "api-key": self.api_key,
            "Content-Type": "application/json"
        }
    
    async def generate_speech(
        self, 
        text: str, 
        voice_id: str = "en-US-daniel",
        style: str = "inspirational",
        speed: float = 1.0,
        pitch: str = "normal"
    ) -> Optional[bytes]:
        """Generate speech using Murf API"""
        try:
            payload = {
                "text": text,
                "voiceId": voice_id,
                "style": style,
                "speakingRate": speed,
                "intonation": pitch,
                "format": "mp3"
            }
            
            response = requests.post(
                f"{self.base_url}/speech/generate",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                print(f"DEBUG: Response content type: {response.headers.get('content-type')}")
                print(f"DEBUG: First 50 bytes: {response.content[:50]}")
                json_response = response.json()
                audio_url = json_response.get('audioFile')
                if audio_url:
                    # Download the audio file from the URL
                    audio_response = requests.get(audio_url)
                    if audio_response.status_code == 200:
                        return audio_response.content
                    else:
                        logger.error(f"Failed to download audio: {audio_response.status_code}")
                        return None
            else:
                logger.error(f"Murf API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating speech: {e}")
            return None