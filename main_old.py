from fastapi import FastAPI, HTTPException
from pytube import YouTube
from dotenv import load_dotenv
from moviepy.editor import AudioFileClip
import whisper
import openai
import os

app = FastAPI()

# Load environment variables (like OpenAI API key)
openai.api_key = os.environ["OPENAI_API_KEY"]

def chunk_text(text, max_length):
    """
    Split the text in chunks that not raised the maximium lenght specific.
    """
    parts = []
    words = text.split()
    current_part = []

    for word in words:
        if len(' '.join(current_part + [word])) <= max_length:
            current_part.append(word)
        else:
            parts.append(' '.join(current_part))
            current_part = [word]

    parts.append(' '.join(current_part))
    return parts

def summarize_chunk(chunk):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Ensure this is a valid model name
            prompt="Summarize the following text:\n\n" + chunk,
            max_tokens=150  # Adjust as needed
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error during summarization: {e}")
        return "Error"  # Return a string for error cases

@app.post("/process-video/")
async def process_video(youtube_url: str):
    # Step 1: Download video and extract audio
    try:
        yt = YouTube(youtube_url)
        video = yt.streams.filter(only_audio=True).first()
        video.download(filename='audio.mp4')
        audio_clip = AudioFileClip('audio.mp4')
        audio_clip.write_audiofile('audio.wav')
        audio_clip.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Step 2: Transcribe audio to text using Whisper
    try:
        model = whisper.load_model("base")
        result = model.transcribe('audio.wav')
        transcribed_text = result["text"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Step 3: Summarize the transcribed text
    try:
        max_length = 1000  # Adjust based on average token size and model's token limit

        chunks = chunk_text(transcribed_text, max_length)
        summaries = [summarize_chunk(chunk) for chunk in chunks]
        summary = " ".join(summaries).replace("\n\n", " ").strip()
        final_summary = summarize_chunk(summary)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

