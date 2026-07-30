from sentence_transformers import CrossEncoder
from src.config import RERANK_MODEL

class Reranker:
    def __init__(self):
        self.model = CrossEncoder(RERANK_MODEL)

    def rerank(self, query, retrieved_chunks, top_k = 6):

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
        return [
            chunk[0]
            for chunk in top_chunks
        ]
