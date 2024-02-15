from db_config.mongo_config import get_database

def get_existing_data(video_id, data_type=None):
    """
    Fetches existing data for a video_id. If data_type is specified,
    returns specific data; otherwise, checks if the video exists.
    """
    db = get_database()
    collection = db['summaries']
    projection = {data_type: 1} if data_type else {}  # Project only specific data_type if provided
    document = collection.find_one({"_id": video_id}, projection)
    
    if not document:
        return None  # Video does not exist
    if data_type:
        return document.get(data_type)  # Return specific data type or None if not found
    return document  # Return the whole document if data_type is not specified

def save_data(video_id, data, data_type):
    """
    Saves specific type of data (metadata, transcription, summary) for a video_id.
    """
    db = get_database()
    collection = db['summaries']
    try:
        collection.update_one({"_id": video_id}, {"$set": {data_type: data}}, upsert=True)
        return True
    except Exception as e:
        print(f"Error saving {data_type}: {e}")
        return False
