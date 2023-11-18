from fastapi import APIRouter, HTTPException, UploadFile, File
import json
import os

router = APIRouter()

SUMMARIES_DIR = 'data/summaries'

@router.post("/upload/", response_description="Upload a video summary")
async def upload_summary(video_id: str, summary: UploadFile = File(...)):
    """
    Uploads a summary for a specific video.
    """
    content = await summary.read()
    summary_text = content.decode("utf-8")

    summary_file_path = os.path.join(SUMMARIES_DIR, f"{video_id}.txt")
    with open(summary_file_path, 'w') as file:
        file.write(summary_text)
    
    return {"message": "Summary uploaded successfully", "video_id": video_id}

@router.get("/{video_id}", response_description="Get video summary")
def get_summary(video_id: str):
    """
    Retrieves the summary for a specific video.
    """
    summary_file_path = os.path.join(SUMMARIES_DIR, f"{video_id}.txt")
    if not os.path.exists(summary_file_path):
        raise HTTPException(status_code=404, detail="Summary not found")

    with open(summary_file_path, 'r') as file:
        summary_text = file.read()

    return {"summary": summary_text, "video_id": video_id}
