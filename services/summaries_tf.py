import os
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, GenerationConfig

class SummaryService:
    def __init__(self, model_name='google/flan-t5-base'):
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)

    def chunk_text(self, text, max_chunk_size=1000):
        """
        Splits the text into chunks of a specified maximum size.
        """
        if len(text) <= max_chunk_size:
            return [text]

        sentences = text.split('.')
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            sentence += '.'
            if len(current_chunk) + len(sentence) <= max_chunk_size:
                current_chunk += sentence
            else:
                chunks.append(current_chunk)
                current_chunk = sentence

        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def generate_summary(self, text, max_chunk_size=1000, max_length=150):
        """
        Generates a summary for the given text using FLAN-T5. For long texts, it first breaks them into chunks.
        """
        chunks = self.chunk_text(text, max_chunk_size)
        all_summaries = ""

        for chunk in chunks:
            prompt = f"Summarize the following conversation:\n\n{chunk}\n\nSummary:"
            inputs = self.tokenizer(prompt, return_tensors='pt', max_length=max_length, truncation=True)
            
            # Generation configuration
            generation_config = GenerationConfig(max_length=max_length, do_sample=True, temperature=0.7)
            summary_ids = self.model.generate(inputs['input_ids'], **vars(generation_config))
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            all_summaries += summary + " "

        return all_summaries.strip()
