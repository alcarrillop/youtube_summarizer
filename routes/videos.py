from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
from services.youtube import YouTubeService
import json
import os

router = APIRouter()

VIDEO_METADATA_DIR = 'data/videos'

youtube_service = YouTubeService()

@router.post("/fetch_metadata/")
def fetch_and_save_video_metadata(url: str):
    """
    Endpoint to fetch and save metadata of a YouTube video.
    """
    try:
        metadata = youtube_service.get_video_metadata(url)
        metadata_file_path = f"data/videos/{metadata['video_id']}_metadata.json"
        youtube_service.save_metadata_as_json(metadata, metadata_file_path)
        return {"message": "Metadata fetched and saved successfully", "file_path": metadata_file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/download/")
def download_video(url: str):
    """
    Endpoint to download a YouTube video.
    """
    try:
        video_path = youtube_service.download_video(url)
        return {"message": "Video downloaded successfully", "path": video_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload_metadata/", response_description="Upload video metadata")
async def upload_video_metadata(video_metadata: UploadFile = File(...)):
    """
    Uploads metadata for a video. The metadata should be in JSON format.
    """
    content = await video_metadata.read()
    metadata = json.loads(content)
    video_id = metadata.get("id")
    if not video_id:
        raise HTTPException(status_code=400, detail="Video ID is required in metadata")

    metadata_file_path = os.path.join(VIDEO_METADATA_DIR, f"{video_id}.json")
    with open(metadata_file_path, 'w') as file:
        json.dump(metadata, file)
    
    return {"message": "Video metadata uploaded successfully", "video_id": video_id}

@router.get("/metadata/{video_id}", response_description="Get video metadata")
def get_video_metadata(video_id: str):
    """
    Retrieves metadata for a specific video.
    """
    metadata_file_path = os.path.join(VIDEO_METADATA_DIR, f"{video_id}.json")
    if not os.path.exists(metadata_file_path):
        raise HTTPException(status_code=404, detail="Video metadata not found")

    with open(metadata_file_path, 'r') as file:
        metadata = json.load(file)

    return metadata
