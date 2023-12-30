from fastapi import APIRouter, HTTPException, Form
from services.youtube import YouTubeService
from services.transcriptions import TranscriptionService
from services.summaries_tf import SummaryService
from db_operations import save_transcription  # Import the MongoDB save function
import os

router = APIRouter()

# Initialize services
youtube_service = YouTubeService()
transcription_service = TranscriptionService()
summary_service = SummaryService()

@router.post("/process-youtube-video/")
async def process_youtube_video(youtube_url: str = Form(...)):
    try:
        # Fetch video metadata
        metadata = youtube_service.get_video_metadata(youtube_url)
        
        # Download audio and generate transcription
        audio_file_path = youtube_service.download_audio_for_transcription(youtube_url)
        transcription_file_path = transcription_service.generate_transcription(audio_file_path)

        # Read the transcription text
        with open(transcription_file_path, 'r') as file:
            transcription_text = file.read()
        
        # After transcription, delete the temporary audio file
        os.remove(audio_file_path)

        # Generate summary
        summary_text = summary_service.generate_summary(transcription_text)

        # Save metadata, transcription, and summary to MongoDB
        save_transcription(metadata['video_id'], transcription_text, summary_text, metadata)

        return {
            "message": "Video processed successfully",
            "metadata": metadata,
            "transcription": transcription_text,
            "summary": summary_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
