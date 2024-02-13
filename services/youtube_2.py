from pytube import YouTube
from moviepy.editor import AudioFileClip
import tempfile
import logging

class YouTubeService:
    def __init__(self):
        pass  # Constructor now does nothing but could be used for future enhancements

    def download_audio_for_transcription(self, url):
            """
            Downloads the video's audio directly for transcription, using a temporary file.
            """
            try:
                yt = YouTube(url)
                audio_stream = yt.streams.filter(only_audio=True).first()
                if not audio_stream:
                    raise ValueError("No suitable audio stream found")
                
                # Download audio directly into a temporary file
                with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp_audio_file:
                    audio_stream.download(filename=tmp_audio_file.name)
                    # No need to extract audio since we're downloading the audio stream directly
                    return tmp_audio_file.name
            except Exception as e:
                logging.error(f"Error downloading audio for transcription: {e}")
                raise

    def get_video_metadata(self, url):
        """
        Fetches and returns metadata for a given YouTube video URL.
        """
        try:
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
            }
            return metadata
        except Exception as e:
            logging.error(f"Error fetching video metadata: {e}")
            raise

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
