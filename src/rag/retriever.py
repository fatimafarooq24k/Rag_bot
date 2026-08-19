from src.rag.embedder import create_embeddings
from src.storage.store import load_data
import logging
from uuid import UUID

logger = logging.getLogger(__name__)

def find_relevant_chunks(doc_id: UUID, user_query: str, top_k: int = 5):

    if not isinstance(user_query, str):
        raise TypeError("Query must be a string value.")
    
    if user_query.strip() == "":
        raise ValueError("Please enter your query.")

    if not isinstance(top_k, int):
        raise TypeError("Please enter a positive integer value.")
    
    if top_k <= 0:
        raise ValueError("Enter a valid search number.")

    user_query_with_instruction = "Represent this sentence for searching relevant passages: " + user_query

    query_embedding = create_embeddings([user_query_with_instruction])

    faiss_index, chunks = load_data(doc_id)

    if not chunks:
        logger.warning("No chunks found for retrieval.")
        return []

    if top_k > len(chunks):
        logger.warning("Requested %d chunks exceeds the available chunks limit: %d. Retrieving %d chunks instead.",
                       top_k,
                       len(chunks),
                       len(chunks))
        top_k = len(chunks)


    _, indices = faiss_index.search(query_embedding, top_k)

    indices = indices.flatten()
    retrieved_chunks = []
    for chunk_index in indices:

        retrieved_chunks.append(chunks[chunk_index])

    logger.info("Relevant chunks retrieved successfully. Total chunks: %d",
                len(retrieved_chunks))

    return retrieved_chunks
