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
