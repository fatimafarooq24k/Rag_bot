from sentence_transformers import SentenceTransformer
from src.core.config import settings
import logging

logger = logging.getLogger(__name__)

model = None
def get_model():
    global model
    if model is None:
        model = SentenceTransformer(
            settings.embedding_model
        )
        logger.info("Model Loading complete.")
    return model

def create_embeddings(chunks):

    if not isinstance(chunks, list):
        raise TypeError("Only lists are supported.")
    
    if not chunks:
        raise ValueError("The List of chunks is empty.")

    if not all(isinstance(chunk, str) for chunk in chunks):
        raise TypeError("Each chunk must be a string.")
    
    model = get_model()

    embeddings = model.encode(
        chunks,
        convert_to_numpy=True
        )

    logger.info("Embedding generation completed. Total embeddings: %d",
                len(embeddings))

    return embeddings