from fastapi import FastAPI, HTTPException
from pytube import YouTube
from dotenv import load_dotenv
from moviepy.editor import AudioFileClip
import whisper
import openai
import os

app = FastAPI()

openai.api_key = os.environ["OPENAI_API_KEY"]

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
        transcription = result["text"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Step 3: Summarize the transcription using OpenAI's GPT
    try:
        response = openai.completions.create(
            model="text-davinci-003",
            prompt="Summarize the following text:\n\n" + transcription,
            max_tokens=150
        )
        
        summary = response.choices[0].text.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Step 4: Return the transcription and summary
    return {
        "transcription": transcription,
        "summary": summary
    }

# To run the server use: uvicorn main:app --reload
