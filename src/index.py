from src import loader, chunker, embedder, store

def index_document(document):

    if not document:
        raise ValueError("Enter a valid document.")

    if not isinstance(document, str):
        raise TypeError("Document path not supported. Must be string")


    pages = loader.extract_text_from_file(document)

    all_chunks = []
    for page in pages:
        page_chunks = chunker.chunk_text(page["text"]) 

        for chunk in page_chunks:
            all_chunks.append(
                {
                    "text" : chunk,
                    "page_number" : page["page_number"]
                }
            )

    chunk_texts = []

    for chunk in all_chunks:
        chunk_texts.append(chunk["text"])

    embeddings = embedder.create_embeddings(chunk_texts)

    try:
        store.store_data(all_chunks, embeddings)
    except Exception as e:
        raise RuntimeError("Error occured while storing the data.") from e

    return {
        "status" : "success",
        "chunks_created" : len(all_chunks),
        "embeddings_created" : len(embeddings)
    }



