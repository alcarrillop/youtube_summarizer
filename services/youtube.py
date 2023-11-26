from pytube import YouTube
from moviepy.editor import AudioFileClip
import os
import json

class YouTubeService:
    def __init__(self):
        self.audio_dir = "data/no_sql/audios"
        self.video_dir = "data/no_sql/videos"
        self.metadata_dir = "data/relational/metadata"
        os.makedirs(self.audio_dir, exist_ok=True)
        os.makedirs(self.video_dir, exist_ok=True)
        os.makedirs(self.metadata_dir, exist_ok=True)

    def download_video(self, url):
        """
        Downloads the video and saves it in the designated directory.
        """
        yt = YouTube(url)
        video = yt.streams.filter(progressive=True, file_extension='mp4').first()
        if video:
            video_file_path = os.path.join(self.video_dir, f"{yt.video_id}.mp4")
            video.download(output_path=self.video_dir, filename=f"{yt.video_id}.mp4")
            return video_file_path
        else:
            raise Exception("No suitable video stream found")

    def extract_audio(self, video_file_path):
        """
        Extracts audio from the downloaded video and saves it as a .wav file.
        """
        audio_clip = AudioFileClip(video_file_path)
        audio_file_path = os.path.join(self.audio_dir, os.path.basename(video_file_path).replace('.mp4', '.wav'))
        audio_clip.write_audiofile(audio_file_path)
        audio_clip.close()
        return audio_file_path

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