from src.store import store_data, load_data
import numpy as np
import pytest

def generate_data():
    chunks = []
    embeddings = []

    for i in range(1, 13):
        chunks.append(f"Chunk {i}")
        embeddings.append(np.random.rand(384))


    return chunks, embeddings

def test_store_data():
    test1_chunks, test1_embeddings = generate_data()

    test1_embeddings = np.array(test1_embeddings)

    store_data(test1_chunks, test1_embeddings)
    index, loaded_chunks = load_data()

    assert index.ntotal == len(test1_chunks)
    assert loaded_chunks == test1_chunks

def test_store_data_invalid_embedding_datatype():
    test2_chunks, test2_embeddings = generate_data()
    with pytest.raises(TypeError):
        store_data(test2_chunks, test2_embeddings)

def test_store_data_invalid_chunks_data_structure():
    test2_chunks, test2_embeddings = "hello", np.array(np.random.rand(384))
    with pytest.raises(TypeError):
        store_data(test2_chunks, test2_embeddings)

def test_store_data_invalid_chunk_datatype():
    test2_chunks, test2_embeddings = [32], np.array(np.random.rand(384))
    with pytest.raises(TypeError):
        store_data(test2_chunks, test2_embeddings)

def test_store_data_empty_chunks():
    test2_chunks, test2_embeddings = [], np.array(np.random.rand(384))
    with pytest.raises(ValueError):
        store_data(test2_chunks, test2_embeddings)

def test_store_data_empty_embeddings():
    test2_chunks, test2_embeddings = ["32"], np.array([])
    with pytest.raises(ValueError):
        store_data(test2_chunks, test2_embeddings)

def test_store_data_dimension_error():
    test1_chunks, test1_embeddings = generate_data()
    test1_embeddings = np.array(test1_embeddings)
    test1_embeddings = np.random.rand(384)
    with pytest.raises(ValueError):
        store_data(test1_chunks, test1_embeddings)


def test_store_data_length_mismatch():
    test1_chunks, test1_embeddings = generate_data()
    test1_embeddings = np.array(test1_embeddings)
    test1_chunks.pop()
    with pytest.raises(ValueError):
        store_data(test1_chunks, test1_embeddings)