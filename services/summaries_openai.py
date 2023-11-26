import os
import openai
from dotenv import load_dotenv

class SummaryService:
    def __init__(self, storage_dir="data/relational/summaries", model_name='text-davinci-003'):
        load_dotenv()
        self.storage_dir = storage_dir
        self.model_name = model_name
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.openai_api_key
        os.makedirs(storage_dir, exist_ok=True)

    def chunk_text(self, text, max_chunk_size=4000):
        """
        Splits the text into chunks, each no longer than a specified maximum size.
        """
        if len(text) <= max_chunk_size:
            return [text]

        sentences = text.split('.')
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk + sentence) < max_chunk_size:
                current_chunk += sentence + '.'
            else:
                chunks.append(current_chunk)
                current_chunk = sentence + '.'

        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def generate_summary(self, text, max_chunk_size=4000, summary_length=50):
        """
        Generates a summary using OpenAI's GPT model. For long texts, it first breaks them into chunks.
        """
        chunks = self.chunk_text(text, max_chunk_size)
        all_summaries = ""

        for chunk in chunks:
            prompt = f"Summarize the following text in {summary_length} words:\n\n{chunk}"
            response = openai.Completion.create(
                model=self.model_name,  # Specify the model here
                prompt=prompt,
                max_tokens=summary_length
            )
            summary = response.choices[0].text.strip()
            all_summaries += summary + " "

        return all_summaries.strip()

    def save_summary(self, summary, summary_file_name):
        """
        Saves the summary text to a file.
        """
        summary_file_path = os.path.join(self.storage_dir, summary_file_name + ".txt")
        with open(summary_file_path, 'w') as file:
            file.write(summary)
        return summary_file_path
