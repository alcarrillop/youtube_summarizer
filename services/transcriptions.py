import os
import whisper

class TranscriptionService:
    def __init__(self, storage_dir="data/relational/transcriptions"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def generate_transcription(self, audio_file_path):
        """
        Generates a transcription for the given audio file and saves it.
        """
        try:
            transcription_text = self.transcribe_audio(audio_file_path)
            transcription_file_path = os.path.join(self.storage_dir, os.path.basename(audio_file_path) + ".txt")
            with open(transcription_file_path, 'w') as file:
                file.write(transcription_text)

            return transcription_file_path
        except Exception as e:
            # You can handle the exception more gracefully here if needed
            raise Exception(f"Error during transcription: {str(e)}")

    def transcribe_audio(self, audio_file_path):
        """
        Transcribes the audio file using Whisper.
        """
        model = whisper.load_model("base")
        result = model.transcribe(audio_file_path)
        return result["text"]

    # Additional methods related to transcription can be added here
