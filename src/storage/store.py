import faiss
import pickle as pkl
import numpy as np
import logging

from src.core.config import settings
from src.storage.paths import get_document_paths

logger = logging.getLogger(__name__)


def store_data(doc_id, chunks, embeddings):

    if not isinstance(chunks, list):
        raise TypeError("Chunks must be a List.")

    if not chunks:
        raise ValueError("Empty Chunk Dictionary")

    paths = get_document_paths(doc_id)
    paths.folder.mkdir(parents=True, exist_ok=True)

    for chunk in chunks:

        if not isinstance(chunk, dict):
            raise TypeError("Each chunk must be a dictionary.")

        if "text" not in chunk:
            raise ValueError("Chunk is missing 'text' field.")

        if "page_number" not in chunk:
            raise ValueError("Chunk is missing 'page_number' field.")

        if not isinstance(chunk["text"], str) :
            raise TypeError("Each chunk must be a string.")
        
        if not isinstance(chunk["page_number"], int):
            raise TypeError("Page number must be a valid number.")

    
    if len(chunks) != len(embeddings):
        raise ValueError("Chunks and embeddings should be of same size.")

    if not isinstance(embeddings, np.ndarray):
        raise TypeError("Embeddings must be a NumPy Array.")

    if embeddings.size == 0:
        raise ValueError("No embeddings found.")

    if embeddings.ndim != 2:
        raise ValueError("Embeddings should be 2D")

    dimension = embeddings.shape[1]
    index = faiss.IndexHNSWFlat(dimension, settings.hnsw_m)
    index.hnsw.efConstruction = settings.hnsw_ef_construction

    logger.info("Index initialized.")
    

    embeddings = embeddings.astype(np.float32)
    index.add(embeddings)

    logger.info("Embeddings stored successfully.")

    faiss.write_index(index, str(paths.index))

    with open(paths.chunks, "wb") as file:
        pkl.dump(chunks, file)

    logger.info("Chunks stored successfully")

def load_data(doc_id):

    paths = get_document_paths(doc_id)

    if not paths.index.is_file():
        raise FileNotFoundError(f"Index does not exist for document id: {doc_id}")

    if not paths.chunks.is_file():
        raise FileNotFoundError(f"Chunks do not exist for document id: {doc_id}")

    index = faiss.read_index(str(paths.index))

    with open(paths.chunks, "rb") as file:
        chunks = pkl.load(file)

    if not isinstance(chunks, list):
        raise TypeError("Chunks must be a List.")

    if not chunks:
        raise ValueError("Empty Chunk List")
    
    for chunk in chunks:
        if not isinstance(chunk, dict):
            raise TypeError("Each chunk must be a dictionary.")

        if "text" not in chunk:
            raise ValueError("Chunk is missing 'text' field.")

        if "page_number" not in chunk:
            raise ValueError("Chunk is missing 'page_number' field.")

        if not isinstance(chunk["text"], str):
            raise TypeError("Each chunk must be a string.")
        
        if not isinstance(chunk["page_number"], int):
            raise TypeError("Page number must be a valid number.")

    index.hnsw.efSearch = settings.hnsw_ef_search

    logger.info("Chunks loaded successfully.")

    return index, chunks