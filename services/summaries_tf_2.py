from transformers import pipeline

class SummaryService:
    def __init__(self):
        # Initialize the summarization pipeline with your chosen model
        self.summarizer = pipeline("summarization", model="Falconsai/text_summarization")

    def chunk_text(self, text, max_chunk_size=1000):
        """
        Splits the text into chunks of a specified maximum size, ensuring not to break sentences.
        """
        sentences = text.split('.')
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            sentence = sentence.strip() + '.'
            if not sentence.strip():
                continue  # Skip empty sentences
            if len(current_chunk) + len(sentence) <= max_chunk_size:
                current_chunk += " " + sentence if current_chunk else sentence
            else:
                chunks.append(current_chunk)
                current_chunk = sentence

        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def generate_summary(self, text, max_chunk_size=1000, max_length=150, min_length=30):
        """
        Generates a summary for the given text by summarizing individual chunks and combining them.
        """
        chunks = self.chunk_text(text, max_chunk_size)
        chunk_summaries = []

        for chunk in chunks:
            summary = self.summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
            chunk_summaries.append(summary[0]['summary_text'])

        # Combine the summaries of all chunks into a single summary
        final_summary = ' '.join(chunk_summaries)
        return final_summary
