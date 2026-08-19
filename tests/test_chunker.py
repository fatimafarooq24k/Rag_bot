from src.rag.chunker import chunk_text
import pytest

valid_text = "The Blossom of flowers in spring is truely a wonderful sight."
empty_text = ""
invalid_text = 45

def test_normal_chunking():
    chunks = chunk_text(valid_text, chunk_size = 7)
    assert len(chunks) == 7

def test_invalid_chunk_size():
     with pytest.raises(ValueError):
         chunk_text(valid_text, chunk_size=-1)

def test_larger_than_text_chunk_size():
    chunks = chunk_text(valid_text, chunk_size=90)
    assert len(chunks) == len()

def test_empty_text():
    with pytest.raises(ValueError):
        chunk_text(empty_text, chunk_size=5)

def test_invalid_text_type():
    with pytest.raises(TypeError):
        chunk_text(invalid_text)

