from src.embedder import create_embeddings
from src.store import load_data
import numpy as np


def find_relevant_chunks(user_query, top_k=5):

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

    faiss_index, chunks = load_data()

    if top_k > len(chunks):
        top_k = len(chunks)

    _, indices = faiss_index.search(query_embedding, top_k)

    indices = indices.flatten()
    retrieved_chunks = []
    for chunk_index in indices:

        retrieved_chunks.append(chunks[chunk_index])

    return retrieved_chunks
