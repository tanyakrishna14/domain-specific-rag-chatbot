from typing import List, Dict, Any
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


class FAISSVectorStore:
    """Small FAISS wrapper for chunk embeddings and metadata."""

    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.embedder = SentenceTransformer(model_name)
        self.index = None
        self.chunks: List[Dict[str, Any]] = []

    def build(self, chunks: List[Dict[str, Any]]):
        self.chunks = chunks
        texts = [item["text"] for item in chunks]

        embeddings = self.embedder.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        ).astype("float32")

        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)
        return self

    def search(self, query: str, top_k=5):
        if self.index is None or not self.chunks:
            return []

        query_embedding = self.embedder.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        ).astype("float32")

        k = min(top_k, len(self.chunks))
        scores, indices = self.index.search(query_embedding, k)

        results = []
        for score, index in zip(scores[0], indices[0]):
            if index < 0:
                continue
            item = dict(self.chunks[index])
            item["score"] = float(score)
            results.append(item)

        return results
