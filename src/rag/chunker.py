import logging

logger = logging.getLogger(__name__)

def chunk_text(text, chunk_size = 500, overlap = 100, max_extension = 50):

    if not text:
        raise ValueError("Text is Empty!")

    if chunk_size <= 0:
        raise ValueError("The chunk size must be greater than 0")
    
    if overlap >= chunk_size:
        raise ValueError("Overlap should be smaller than the chunk size.")

    if (overlap > chunk_size/2):
        raise ValueError("Overlap should not be greater than half of the chunk size.")


    text_chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        extension = 0
        while (
            end < len(text)
             and text[end].isspace()
             and extension < max_extension
        ): 
            end += 1
            extension += 1

        chunk = text[start:end].strip()
        if chunk:
            text_chunks.append(chunk) 
        if end == len(text):
            break

        start = end - overlap
        while (
            start != 0
            and text[start-1].isspace()
               ):
            start -= 1

    return text_chunks

