from pytube import YouTube
from moviepy.editor import AudioFileClip
import os
import json
import tempfile 

class YouTubeService:
    def __init__(self):
        self.audio_dir = "data/no_sql/audios"
        self.video_dir = "data/no_sql/videos"
        self.metadata_dir = "data/relational/metadata"
        os.makedirs(self.audio_dir, exist_ok=True)
        os.makedirs(self.video_dir, exist_ok=True)
        os.makedirs(self.metadata_dir, exist_ok=True)

    def download_audio_for_transcription(self, url):
        """
        Downloads the video, extracts audio, and saves it temporarily for transcription.
        """
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        if video:
            with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp_video_file:
                video_file_path = tmp_video_file.name
                video.download(filename=video_file_path)

            # Extract audio
            audio_clip = AudioFileClip(video_file_path)
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_audio_file:
                audio_file_path = tmp_audio_file.name
                audio_clip.write_audiofile(audio_file_path)

            # Remove the temporary video file
            os.remove(video_file_path)

            return audio_file_path
        else:
            raise Exception("No suitable audio stream found")
        
    def get_video_metadata(self, url):
        """
        Fetches metadata for a given YouTube video URL.
        """
        yt = YouTube(url)
        metadata = {
            "video_id": yt.video_id,
            "title": yt.title,
            "description": yt.description,
            "length": yt.length,
            "views": yt.views,
            "rating": yt.rating,
            "author": yt.author,
            "publish_date": str(yt.publish_date),
            # Add more attributes as needed
        }
        return metadata

    def save_metadata_as_json(self, metadata):
        """
        Saves the video metadata as a JSON file in the designated directory.
        """
        file_path = os.path.join(self.metadata_dir, f"{metadata['video_id']}_metadata.json")
        with open(file_path, 'w') as json_file:
            json.dump(metadata, json_file, indent=4)