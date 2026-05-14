import os
import hashlib
from typing import List, Dict, Any, Optional

from app.config import settings


class EmbeddingManager:
    def __init__(self):
        self.model = None
        self.initialized = False
        self.embedding_cache: Dict[str, List[float]] = {}

    async def initialize(self):
        if self.initialized:
            return
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(
                settings.embedding_model,
                device="cpu",
            )
            self.model.max_seq_length = 512
            self.initialized = True
        except Exception as e:
            print(f"Failed to load embedding model: {e}")
            raise

    def embed(self, text: str) -> List[float]:
        cache_key = hashlib.md5(text.encode()).hexdigest()
        if cache_key in self.embedding_cache:
            return self.embedding_cache[cache_key]

        if not self.initialized:
            raise RuntimeError("Embedding model not initialized")

        embedding = self.model.encode(text, normalize_embeddings=True).tolist()
        self.embedding_cache[cache_key] = embedding
        return embedding

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        if not self.initialized:
            raise RuntimeError("Embedding model not initialized")
        return [self.embed(t) for t in texts]


def chunk_text(text: str, chunk_size: int = 800, chunk_overlap: int = 120) -> List[str]:
    if not text or len(text.strip()) == 0:
        return []

    sentences = text.replace("\n\n", "\n").split("\n")
    sentences = [s.strip() for s in sentences if s.strip()]

    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_len = len(sentence)

        if current_length + sentence_len > chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            overlap_start = max(0, len(current_chunk) - chunk_overlap // 40)
            current_chunk = current_chunk[overlap_start:]
            current_length = sum(len(s) for s in current_chunk)

        current_chunk.append(sentence)
        current_length += sentence_len

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
