from src.retriever import find_relevant_chunks
from src.store import load_data
import pytest

valid_query = "I want to know about AI"
invalid_type_query = 32
white_space_queries = ["", "\t", "\n"]

valid_top_k = 2
invalid_top_k = [-6, 0] 
invalid_type_top_k = "5"
larger_than_chunk_count_top_k = 90

def test_retriever_workflow():
    retrieved_chunks = find_relevant_chunks(valid_query, valid_top_k)
    assert isinstance(retrieved_chunks, list)
    assert len(retrieved_chunks) > 0
    assert all(isinstance(chunk, str) for chunk in retrieved_chunks)
    assert len(retrieved_chunks) == valid_top_k


def test_retriever_query_type():
    with pytest.raises(TypeError):
        find_relevant_chunks(invalid_type_query, valid_top_k)

def test_retriever_empty_query_type():
    for i in white_space_queries:
        with pytest.raises(ValueError):
            find_relevant_chunks(i, valid_top_k)

def test_retriever_top_k_type():
    with pytest.raises(TypeError):
        find_relevant_chunks(valid_query, invalid_type_top_k)

def test_retriever_top_k_invalid_number():
    for i in invalid_top_k:
        with pytest.raises(ValueError):
            find_relevant_chunks(valid_query, i)

def test_retriever_top_k_greater_than_chunk_number():
    _, total_chunks = load_data()
    retrieved_chunks = find_relevant_chunks(valid_query, larger_than_chunk_count_top_k)
    assert len(total_chunks) == len(retrieved_chunks)
