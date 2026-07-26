def chunk_text(text, chunk_size = 500, max_extension = 50):
    if not text:
        raise ValueError("Text is Empty!")

    if chunk_size <= 0:
        raise ValueError("The chunk size must be greater than 0")
    
    text_chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        extension = 0
        while (
            end < len(text)
             and text[end] != " " 
             and extension < max_extension
        ): 
            end += 1
            extension += 1

        chunk = text[start:end].strip()

        if chunk:
            text_chunks.append(chunk) 
        start = end

    return text_chunks

