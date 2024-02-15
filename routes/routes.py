from fastapi import APIRouter, HTTPException, Form
from services.youtube_2 import YouTubeService
from services.transcriptions_2 import TranscriptionService
from services.summaries_tf_2 import SummaryService
from db_config.db_operations import get_existing_data, save_data
import os

router = APIRouter()

# Initialize services
youtube_service = YouTubeService()
transcription_service = TranscriptionService()
summary_service = SummaryService()

@router.post("/metadata/")
async def process_metadata(youtube_url: str = Form(...)):
    metadata = youtube_service.get_video_metadata(youtube_url)
    video_id = metadata.get('video_id')
    
    if not video_id:
        raise HTTPException(status_code=400, detail="Unable to extract video ID.")

    existing_metadata = get_existing_data(video_id, "metadata")
    if existing_metadata:
        return {"message": "Metadata already exists.", "metadata": existing_metadata}
    
    if save_data(video_id, metadata, "metadata"):
        return {"message": "Metadata processed successfully", "metadata": metadata}
    else:
        raise HTTPException(status_code=500, detail="Failed to save metadata.")

@router.post("/transcription/")
async def process_transcription(video_id: str = Form(...)):
    existing_transcription = get_existing_data(video_id, "transcription")
    if existing_transcription:
        return {"message": "Transcription already exists.", "transcription": existing_transcription}

    # Assuming there's a mechanism in place to fetch the youtube_url based on video_id
    # This requires you to have the youtube_url saved with the metadata initially
    youtube_url = get_existing_data(video_id, "metadata").get('youtube_url')
    if not youtube_url:
        raise HTTPException(status_code=400, detail="YouTube URL is required for processing transcription.")

    try:
        
        audio_file_path = youtube_service.download_audio_for_transcription(youtube_url)
    except Exception as e:
        raise  HTTPException(status_code=503, detail=f"Error downloading audio file: {str(e)}")
        
    try:
        transcription = transcription_service.generate_transcription(audio_file_path)
        os.remove(audio_file_path)  # Clean up temporary file
    except Exception as e:
        raise  HTTPException(status_code=503, detail=f"Failed to save transcription. Error: {str(e)}")
        
    
    if save_data(video_id, transcription, "transcription"):
        return {"message": "Transcription processed successfully", "transcription": transcription}
    else:
        raise HTTPException(status_code=500, detail="Failed to save transcription.")

@router.post("/summary/")
async def process_summary(video_id: str = Form(...), transcription: str = Form(None)):
    existing_summary = get_existing_data(video_id, "summary")
    if existing_summary:
        return {"message": "Summary already exists.", "summary": existing_summary}

    # If transcription is not provided, attempt to fetch the existing transcription
    if not transcription:
        transcription = get_existing_data(video_id, "transcription")
        if not transcription:
            raise HTTPException(status_code=400, detail="Transcription not found for processing summary.")
        
    summary = summary_service.generate_summary(transcription)
    if save_data(video_id, summary, "summary"):
        return {"message": "Summary processed successfully", "summary": summary}
    else:
        raise HTTPException(status_code=500, detail="Failed to save summary.")
