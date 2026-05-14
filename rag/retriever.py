import os
import json
from typing import List, Dict, Any, Optional

from app.config import settings


class Retriever:
    def __init__(self, embedding_manager):
        self.embedding_manager = embedding_manager
        self.vector_store = None
        self.documents: List[Dict[str, Any]] = []
        self.initialized = False
        self.cache: Dict[str, List[Dict[str, Any]]] = {}

    async def initialize(self):
        if self.initialized:
            return
        await self._init_vector_store()
        self.initialized = True

    async def _init_vector_store(self):
        persist_dir = os.path.abspath(settings.chroma_db_dir)
        os.makedirs(persist_dir, exist_ok=True)

        if settings.vector_db == "chroma":
            try:
                import chromadb
                from chromadb.config import Settings as ChromaSettings

                client = chromadb.PersistentClient(
                    path=persist_dir,
                    settings=ChromaSettings(
                        anonymized_telemetry=False,
                        allow_reset=True,
                    ),
                )
                collection_name = "flashoot"
                try:
                    self.vector_store = client.get_collection(collection_name)
                except:
                    self.vector_store = client.create_collection(collection_name)

                self.chroma_client = client
                self.collection_name = collection_name
            except ImportError:
                self.vector_store = None
        else:
            try:
                import faiss
                import numpy as np
                self.faiss_index = faiss.IndexFlatIP(384)
                self.faiss_docs = []
                self.faiss_id = 0
            except ImportError:
                self.faiss_index = None

    async def index_chunks(self, chunks: List[Dict[str, Any]]):
        if not chunks:
            return

        self.documents.extend(chunks)
        texts = [c["text"] for c in chunks]
        urls = [c["url"] for c in chunks]
        metadatas = [{"url": url, "title": f"Flashoot - {url}"} for url in urls]

        embeddings = self.embedding_manager.embed_batch(texts)

        if settings.vector_db == "chroma" and self.vector_store is not None:
            ids = [f"chunk_{hash(t)}" for t in texts]
            existing = set()
            try:
                existing_data = self.vector_store.get(ids=ids)
                if existing_data and existing_data["ids"]:
                    existing = set(existing_data["ids"])
            except:
                pass

            new_ids = []
            new_embeddings = []
            new_texts = []
            new_metadatas = []

            for i, doc_id in enumerate(ids):
                if doc_id not in existing:
                    new_ids.append(doc_id)
                    new_embeddings.append(embeddings[i])
                    new_texts.append(texts[i])
                    new_metadatas.append({**metadatas[i], "text": texts[i]})

            if new_ids:
                self.vector_store.add(
                    ids=new_ids,
                    embeddings=new_embeddings,
                    documents=new_texts,
                    metadatas=new_metadatas,
                )
        elif settings.vector_db == "faiss" and hasattr(self, "faiss_index") and self.faiss_index is not None:
            import numpy as np
            emb_array = np.array(embeddings).astype(np.float32)
            self.faiss_index.add(emb_array)
            for i, chunk in enumerate(chunks):
                self.faiss_docs.append({
                    "id": self.faiss_id,
                    "text": chunk["text"],
                    "url": chunk["url"],
                })
                self.faiss_id += 1

        self.cache.clear()

    async def retrieve(self, query: str, k: Optional[int] = None) -> List[Dict[str, Any]]:
        k = k or settings.top_k_results

        cache_key = f"{query}:{k}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        query_embedding = self.embedding_manager.embed(query)

        results = []
        if settings.vector_db == "chroma" and self.vector_store is not None:
            try:
                response = self.vector_store.query(
                    query_embeddings=[query_embedding],
                    n_results=k,
                    include=["documents", "metadatas", "distances"],
                )
                if response and response["documents"] and len(response["documents"]) > 0:
                    for i in range(len(response["documents"][0])):
                        results.append({
                            "text": response["documents"][0][i],
                            "url": response["metadatas"][0][i].get("url", ""),
                            "title": response["metadatas"][0][i].get("title", ""),
                            "score": response["distances"][0][i] if response.get("distances") else 0.0,
                        })
            except Exception as e:
                print(f"Chroma query error: {e}")
        elif settings.vector_db == "faiss" and hasattr(self, "faiss_index") and self.faiss_index is not None:
            import numpy as np
            emb_array = np.array([query_embedding]).astype(np.float32)
            scores, indices = self.faiss_index.search(emb_array, min(k, len(self.faiss_docs)))
            for i, idx in enumerate(indices[0]):
                if idx >= 0 and idx < len(self.faiss_docs):
                    doc = self.faiss_docs[idx]
                    results.append({
                        "text": doc["text"],
                        "url": doc["url"],
                        "score": float(scores[0][i]),
                    })

        if not results and self.documents:
            import numpy as np
            query_emb = np.array(query_embedding)
            scored = []
            for doc in self.documents:
                doc_emb = np.array(self.embedding_manager.embed(doc["text"]))
                score = np.dot(query_emb, doc_emb)
                scored.append((score, doc))
            scored.sort(key=lambda x: x[0], reverse=True)
            for score, doc in scored[:k]:
                results.append({
                    "text": doc["text"],
                    "url": doc["url"],
                    "score": float(score),
                })

        self.cache[cache_key] = results
        return results

    def get_sources(self) -> List[Dict[str, Any]]:
        seen = set()
        sources = []
        for doc in self.documents:
            url = doc.get("url", "")
            if url and url not in seen:
                seen.add(url)
                sources.append({"url": url, "chunks": sum(1 for d in self.documents if d.get("url") == url)})
        return sources
