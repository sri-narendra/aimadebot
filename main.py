import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.api import router

from utils.rate_limiter import RateLimiterMiddleware
from utils.security import SecurityMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    from rag.embeddings import EmbeddingManager
    app.state.embedding_manager = EmbeddingManager()
    await app.state.embedding_manager.initialize()
    from rag.retriever import Retriever
    app.state.retriever = Retriever(app.state.embedding_manager)
    from services.llm_service import LLMService
    app.state.llm_service = LLMService(app.state.retriever)
    from services.crawler import CrawlerService
    app.state.crawler_service = CrawlerService()
    
    # Auto-ingest on startup
    try:
        result = await app.state.crawler_service.crawl()
        raw_content = result["content"]
        
        from rag.embeddings import chunk_text
        chunks = []
        for url, text in raw_content.items():
            page_chunks = chunk_text(
                text,
                chunk_size=settings.chunk_size,
                chunk_overlap=settings.chunk_overlap,
            )
            for c in page_chunks:
                chunks.append({"url": url, "text": c})
        
        # Load data.json
        data_json_path = "/app/data/flashoot_data.json"
        if os.path.exists(data_json_path):
            import json
            with open(data_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            from app.api import _extract_datajson_chunks
            data_chunks = _extract_datajson_chunks(data)
            for chunk in data_chunks:
                text_chunks = chunk_text(chunk["text"], chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap)
                for tc in text_chunks:
                    chunks.append({"url": chunk["url"], "text": tc})
        
        await app.state.retriever.index_chunks(chunks)
        print(f"Auto-ingested {len(chunks)} chunks on startup")
    except Exception as e:
        print(f"Auto-ingest skipped: {e}")
    
    yield


app = FastAPI(
    title="Flashoot AI Chatbot",
    description="RAG-powered chatbot for Flashoot website content",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.allowed_origin] if settings.allowed_origin != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RateLimiterMiddleware)
app.add_middleware(SecurityMiddleware)

app.include_router(router)


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
