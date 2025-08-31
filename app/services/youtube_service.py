from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp
import os
import logging
from typing import Optional, Dict, Any
import re

logger = logging.getLogger(__name__)

class YouTubeService:
    def __init__(self):
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': './data/audio/temp_%(id)s.%(ext)s',
            'quiet': True,
            'no_warnings': True
        }
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from YouTube URL"""
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([^&\n?#]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    async def get_transcript(self, video_url: str) -> Optional[str]:
        """Get transcript from YouTube video"""
        try:
            video_id = self.extract_video_id(video_url)
            if not video_id:
                return None
            try:
                transcript = YouTubeTranscriptApi().fetch(video_id)
                return ' '.join([entry.text for entry in transcript])
            except Exception as e:
                logger.warning(f"Could not get transcript directly: {e}")
                # Fallback to audio download and transcription
                audio_path = await self.download_audio(video_url)
                if audio_path:
                    # Use AssemblyAI for transcription
                    from services.assembly_service import AssemblyService
                    assembly_service = AssemblyService()
                    transcript = await assembly_service.transcribe_audio(audio_path)
                    # Clean up temporary file
                    if os.path.exists(audio_path):
                        os.remove(audio_path)
                    return transcript
                return None
            
        except Exception as e:
            logger.error(f"Error getting transcript: {e}")
            return None
    
    async def get_video_info(self, video_url: str) -> Dict[str, Any]:
        """Get video information"""
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(video_url, download=False)
                if not info:
                    logger.error("yt_dlp.extract_info returned None")
                    return {}
                return {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'description': info.get('description', ''),
                    'uploader': info.get('uploader', 'Unknown')
                }
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            return {}
    
    async def download_audio(self, video_url: str) -> Optional[str]:
        """Download audio from YouTube video"""
        try:
            video_id = self.extract_video_id(video_url)
            if not video_id:
                return None
            
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                filename = ydl.prepare_filename(info)
                
                # Find the actual downloaded file
                for ext in ['m4a', 'webm', 'mp3']:
                    test_path = filename.replace('.%(ext)s', f'.{ext}')
                    if os.path.exists(test_path):
                        return test_path
                
                return filename
                
        except Exception as e:
            logger.error(f"Error downloading audio: {e}")
            return None