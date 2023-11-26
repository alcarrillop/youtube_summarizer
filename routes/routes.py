from fastapi import APIRouter, HTTPException, Form
from services.youtube import YouTubeService
from services.transcriptions import TranscriptionService
from services.summaries_tf import SummaryService
import os

router = APIRouter()

# Initialize services
youtube_service = YouTubeService()
transcription_service = TranscriptionService()
summary_service = SummaryService()

@router.post("/process-youtube-video/")
async def process_youtube_video(youtube_url: str = Form(...)):
    try:
        # Fetch and save video metadata
        metadata = youtube_service.get_video_metadata(youtube_url)
        youtube_service.save_metadata_as_json(metadata)

        # Download video and extract audio
        video_file_path = youtube_service.download_video(youtube_url)
        audio_file_path = youtube_service.extract_audio(video_file_path)

        # Transcribe audio and summarize transcription
        transcription_path = transcription_service.generate_transcription(audio_file_path)
        with open(transcription_path, 'r') as file:
            transcription_text = file.read()
        
        summary = summary_service.generate_summary(transcription_text)
        summary_file_name = metadata['video_id'] + "_summary"
        summary_file_path = summary_service.save_summary(summary, summary_file_name)

        return {
            "message": "Video processed successfully",
            "metadata_file": f"{metadata['video_id']}_metadata.json",
            "audio_file": os.path.basename(audio_file_path),
            "video_file": os.path.basename(video_file_path),
            "transcription_file": os.path.basename(transcription_path),
            "summary_file": os.path.basename(summary_file_path)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
