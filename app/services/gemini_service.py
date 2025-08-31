from google import genai
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key)
    
    async def summarize_text(self, text: str, length: str = "medium") -> Optional[str]:
        """Summarize text using Gemini"""
        try:
            prompts = {
                "short": "Summarize this text in 3-5 bullet points, focusing on key information:",
                "medium": "Provide a concise paragraph summary of this text, capturing the main ideas:",
                "long": "Create a detailed summary of this text, preserving important details and context:"
            }
            
            prompt = f"{prompts.get(length, prompts['medium'])}\n\n{text}"
            
            response = self.client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
                )
            return response.text
            
        except Exception as e:
            logger.error(f"Error summarizing text: {e}")
            return None
    
    async def translate_text(self, text: str, target_language: str) -> Optional[str]:
        """Translate text using Gemini"""
        try:
            prompt = f"Translate the following text to {target_language}:\n\n{text}"
            response = self.client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
                )
            return response.text
        except Exception as e:
            logger.error(f"Error translating text: {e}")
            return None