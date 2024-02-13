from fastapi import APIRouter, HTTPException, Form
from services.youtube_2 import YouTubeService
from services.transcriptions_2 import TranscriptionService
from services.summaries_tf_2 import SummaryService
from db_config.db_operations import save_transcription, check_if_video_exists
import os

router = APIRouter()

# Initialize services
youtube_service = YouTubeService()
transcription_service = TranscriptionService()
summary_service = SummaryService()

@router.post("/process-youtube-video/")
async def process_youtube_video(youtube_url: str = Form(...)):
    # Fetch video metadata
    metadata = youtube_service.get_video_metadata(youtube_url)
    if check_if_video_exists(metadata['video_id']):
        raise HTTPException(status_code=400, detail="Video has already been processed.")

    try:
        # Download audio and generate transcription directly
        audio_file_path = youtube_service.download_audio_for_transcription(youtube_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading audio: {str(e)}")

    try:
        transcription = transcription_service.generate_transcription(audio_file_path)
    except Exception as e:
        os.remove(audio_file_path)  # Ensure the audio file is removed even if transcription fails
        raise HTTPException(status_code=500, detail=f"Error generating transcription: {str(e)}")
    
    # Clean up the temporary audio file after use
    os.remove(audio_file_path)

    try:
        # Generate summary
        summary = summary_service.generate_summary(transcription)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")

    # try:
    #     # Attempt to save metadata, transcription, and summary to MongoDB
    #     if not save_transcription(metadata['video_id'], transcription, summary, metadata):
    #         raise HTTPException(status_code=500, detail="Failed to save data to database. Video ID might already exist.")
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Database operation failed: {str(e)}")

    return {
        "message": "Video processed successfully",
        "metadata": metadata,
        "transcription": transcription,
        "summary": summary
    }
