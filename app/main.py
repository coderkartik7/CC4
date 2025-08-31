from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn
import os
import uuid
import aiofiles
from dotenv import load_dotenv
import logging
from pathlib import Path

# Import services
from services.murf_service import MurfService
from services.gemini_service import GeminiService
from services.youtube_service import YouTubeService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="YouTube Summarizer", description="YouTube Video Summarization Platform")

# Initialize services
murf_service = MurfService()
gemini_service = GeminiService()
youtube_service = YouTubeService()

current_dir = Path(__file__).parent.parent
static_path = current_dir / 'static'
data_path = current_dir / 'data' / 'audio'

# Mount static files
app.mount("/static", StaticFiles(directory=static_path), name="static")
app.mount("/data/audio", StaticFiles(directory=data_path), name="audio_files")

# Pydantic model
class SummarizeRequest(BaseModel):
    youtube_url: str
    length: str = "medium"  # "short", "medium", "long"

@app.get("/", response_class=HTMLResponse)
async def homepage():
    """Serve the main HTML page"""
    with open("./templates/index.html", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.post("/api/summarize")
async def summarize_youtube(request: SummarizeRequest):
    print(f"Received request: {request}")
    """Summarize YouTube video"""
    try:
        # Get transcript from YouTube
        transcript = await youtube_service.get_transcript(request.youtube_url)
        
        if not transcript:
            raise HTTPException(status_code=404, detail="Could not extract transcript from video")
        
        # Generate summary
        summary = await gemini_service.summarize_text(transcript, request.length)
        if not summary:
            raise HTTPException(status_code=500, detail="Failed to generate summary")
        
        # Convert summary to speech
        audio_data = await murf_service.generate_speech(
            text=summary,
            voice_id="en-US-daniel"
        )

        print(f"DEBUG: Audio data length: {len(audio_data) if audio_data else 'None'}")
        
        if not audio_data:
            raise HTTPException(status_code=500, detail="Failed to generate audio")
        
        # Save audio file
        filename = f"summary_{uuid.uuid4().hex}.mp3"
        filepath = f"./data/audio/{filename}"
        
        async with aiofiles.open(filepath, 'wb') as f:
            await f.write(audio_data)
        
        # Get video info
        video_info = await youtube_service.get_video_info(request.youtube_url)
        
        return {
            "summary": summary,
            "audio_url": f"/data/audio/{filename}",
            "filename": filename,
            "video_info": video_info
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Summarization error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)