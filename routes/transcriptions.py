from fastapi import APIRouter, HTTPException, UploadFile, File
import json
import os

router = APIRouter()

TRANSCRIPTIONS_DIR = 'data/transcriptions'

@router.post("/upload/", response_description="Upload a video transcription")
async def upload_transcription(video_id: str, transcription: UploadFile = File(...)):
    """
    Uploads a transcription for a specific video.
    """
    content = await transcription.read()
    transcription_text = content.decode("utf-8")

    transcription_file_path = os.path.join(TRANSCRIPTIONS_DIR, f"{video_id}.txt")
    with open(transcription_file_path, 'w') as file:
        file.write(transcription_text)
    
    return {"message": "Transcription uploaded successfully", "video_id": video_id}

@router.get("/{video_id}", response_description="Get video transcription")
def get_transcription(video_id: str):
    """
    Retrieves the transcription for a specific video.
    """
    transcription_file_path = os.path.join(TRANSCRIPTIONS_DIR, f"{video_id}.txt")
    if not os.path.exists(transcription_file_path):
        raise HTTPException(status_code=404, detail="Transcription not found")

    with open(transcription_file_path, 'r') as file:
        transcription_text = file.read()

    return {"transcription": transcription_text, "video_id": video_id}
