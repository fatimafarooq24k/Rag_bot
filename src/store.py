import faiss
import src.config as cf
import pickle as pkl
import numpy as np
from pathlib import Path

def store_data(chunks, embeddings):

    if not isinstance(chunks, list):
        raise TypeError("Chunks must be a List.")
    
    if not all(isinstance(chunk, str) for chunk in chunks):
        raise TypeError("Each chunk must be a string.")

    if not chunks:
        raise ValueError("Empty Chunk List")
    
    if len(chunks) != len(embeddings):
        raise ValueError("Chunks and embeddings should be of same size.")

    if not isinstance(embeddings, np.ndarray):
        raise TypeError("Embeddings must be a NumPy Array.")

    if embeddings.size == 0:
        raise ValueError("No embeddings found.")

    if embeddings.ndim != 2:
        raise ValueError("Embeddings should be 2D")

    dimension = embeddings.shape[1]
    index = faiss.IndexHNSWFlat(dimension, cf.HNSW_M)
    index.hnsw.efConstruction = cf.HNSW_EF_CONSTRUCTION

    embeddings = embeddings.astype(np.float32)
    index.add(embeddings)

    faiss.write_index(index, cf.INDEX_PATH)

    with open(cf.CHUNKS_PATH, "wb") as file:
        pkl.dump(chunks, file)

def load_data():

    if not Path(cf.INDEX_PATH).is_file():
        raise FileNotFoundError(f"File does not exist at path {cf.INDEX_PATH}")

    if not Path(cf.CHUNKS_PATH).is_file():
        raise FileNotFoundError(f"File does not exist at path {cf.CHUNKS_PATH}")

    index = faiss.read_index(cf.INDEX_PATH)

    with open(cf.CHUNKS_PATH, "rb") as file:
        chunks = pkl.load(file)

    if not isinstance(chunks, list):
        raise TypeError("Chunks must be a List.")

    if not chunks:
        raise ValueError("Empty Chunk List")
    
    if not all(isinstance(chunk, str) for chunk in chunks):
        raise TypeError("Each chunk must be a string.")

    return index, chunks