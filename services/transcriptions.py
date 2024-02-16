import whisper

class TranscriptionService:
    def __init__(self):
        self.model = whisper.load_model("base")

    def generate_transcription(self, audio_file_path):
        """
        Generates a transcription for the given audio file.
        """
        try:
            transcription_text = self.transcribe_audio(audio_file_path)
            return transcription_text
        except Exception as e:
            raise Exception(f"Error during transcription: {str(e)}")

    def transcribe_audio(self, audio_file_path):
        """
        Transcribes the audio file using Whisper.
        """
        result = self.model.transcribe(audio_file_path)
        return result["text"]

