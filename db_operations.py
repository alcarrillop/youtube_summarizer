from mongo_config import get_database
from pymongo.errors import DuplicateKeyError

def save_transcription(video_id, transcription, summary, metadata):
    db = get_database()
    collection = db.transcriptions

    try:
        collection.insert_one({
            "_id": video_id,  # Use the video ID as the unique identifier
            "transcription": transcription,
            "summary": summary,
            "metadata": metadata
        })
        return True  # Successfully saved
    except DuplicateKeyError:
        return False  # Document with this ID already exists

def check_if_video_exists(video_id):
    db = get_database()
    collection = db.transcriptions
    return collection.find_one({"_id": video_id}) is not None