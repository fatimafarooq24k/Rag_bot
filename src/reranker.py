from sentence_transformers import CrossEncoder

class Reranker:
    def __init__(self):
        self.model = CrossEncoder("BAAI/bge-reranker-v2-m3")

    def rerank(self, query, retrieved_chunks, top_k = 6):

        pairs = []

        for chunk in retrieved_chunks:
            pairs.append(
                (query, chunk)
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
