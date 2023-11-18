from pytube import YouTube
import os
import json

class YouTubeService:
    def __init__(self, download_dir="downloads"):
        self.download_dir = download_dir
        os.makedirs(download_dir, exist_ok=True)

    def download_video(self, url):
        """
        Downloads the video from the given URL.
        """
        yt = YouTube(url)
        video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if video_stream:
            video_stream.download(output_path=self.download_dir, filename=f"{yt.video_id}.mp4")
            return f"{self.download_dir}/{yt.video_id}.mp4"
        else:
            raise Exception("No suitable video stream found")

    def extract_audio(self, video_path):
        """
        Extracts audio from the downloaded video.
        """
        # Here you can implement the logic to extract audio from the video
        # For example, using moviepy or a similar library
        pass

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

    def save_metadata_as_json(self, metadata, file_path):
        """
        Saves the video metadata as a JSON file.
        """
        with open(file_path, 'w') as json_file:
            json.dump(metadata, json_file, indent=4)
