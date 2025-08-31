import assemblyai as aai
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class AssemblyService:
    def __init__(self):
        self.api_key = os.getenv("ASSEMBLYAI_API_KEY")
        aai.settings.api_key = self.api_key
    
    async def transcribe_audio(self, audio_url: str) -> Optional[str]:
        """Transcribe audio using AssemblyAI"""
        try:
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(audio_url)
            
            if transcript.status == aai.TranscriptStatus.error:
                logger.error(f"Transcription error: {transcript.error}")
                return None
                
            return transcript.text
            
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            return None