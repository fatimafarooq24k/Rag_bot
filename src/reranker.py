from sentence_transformers import CrossEncoder
from src.core.config import settings
import logging

logger = logging.getLogger(__name__)

class Reranker:
    def __init__(self):
        self.model = CrossEncoder(settings.rerank_model)

        logger.info("Reranker model loaded successfully.")

    def rerank(self, query, retrieved_chunks, top_k = 6):
        if not isinstance(top_k, int):
            raise TypeError("top_k must be an integer.")

        if top_k <= 0:
            raise ValueError("top_k must be greater than 0.")

        pairs = []

        for chunk in retrieved_chunks:
            pairs.append(
                (query, chunk["text"])
            )

        scores = self.model.predict(pairs)

        ranked = list(zip(retrieved_chunks, scores))

        ranked.sort(
            key=lambda x: x[1],
            reverse=True
        )

        top_chunks = ranked[:top_k]

        logger.info("Chunks reranked successfully. Total reranked chunks: %d", len(top_chunks))
        return [
            chunk[0]
            for chunk in top_chunks
        ]
