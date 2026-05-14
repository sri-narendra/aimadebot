import json
import os
import time
from typing import Optional

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.config import settings
from utils.security import sanitize_input, detect_injection, validate_prompt

router = APIRouter()

BOT_NAME = "Flashoot Assistant"

CUSTOMER_FRIENDLY_FALLBACK = (
    "Thanks for asking! I don't have that exact detail in my current knowledge base yet, "
    "but Flashoot focuses on fast, high-quality short-form video creation and creator-driven services. "
    "If you'd like, I can share our services, delivery model, and social links."
)

CAPABILITY_RESPONSE = (
    f"I'm {BOT_NAME}, here to help you with Flashoot information! "
    "I can help you with services, pricing packages, booking flow, delivery model, "
    "social links, and company details. "
    "For quick help, ask things like: 'What services do you offer?', "
    "'How fast is delivery?', or 'Share your social media links.'"
)

CAPABILITY_PATTERNS = (
    "what can you do",
    "what do you do",
    "how can you help",
    "your services",
    "services you offer",
    "who are you",
    "what are you",
    "help me",
    "your capabilities",
)


class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    conversation_id: Optional[str] = None


class IngestionResponse(BaseModel):
    status: str
    pages_crawled: int
    chunks_created: int
    message: str


def _is_capability_question(message: str) -> bool:
    msg = message.lower()
    return any(pattern in msg for pattern in CAPABILITY_PATTERNS)


@router.get("/health")
async def health():
    return {
        "status": "healthy",
        "provider": settings.llm_provider,
        "vector_db": settings.vector_db,
        "top_k": settings.top_k_results,
        "fallback_enabled": settings.enable_provider_fallback,
        "bot_name": BOT_NAME,
    }


@router.get("/sources")
async def sources(request: Request):
    retriever = request.app.state.retriever
    return retriever.get_sources()


@router.post("/chat")
async def chat(request: Request, body: ChatMessage):
    start_time = time.time()

    sanitized = sanitize_input(body.message)
    if detect_injection(sanitized):
        return StreamingResponse(
            _stream_error("I can only answer questions about Flashoot website content."),
            media_type="text/event-stream",
        )

    validation = validate_prompt(sanitized)
    if not validation["allowed"]:
        return StreamingResponse(
            _stream_error(validation["response"]),
            media_type="text/event-stream",
        )

    llm_service = request.app.state.llm_service
    retriever = request.app.state.retriever

    user_message = validation["cleaned_message"]

    # Check for capability questions
    if _is_capability_question(user_message):
        async def capability_generator():
            for word in CAPABILITY_RESPONSE.split():
                yield f"data: {json.dumps({'type': 'content', 'content': word + ' '})}\n\n"
            yield "data: [DONE]\n\n"
        return StreamingResponse(capability_generator(), media_type="text/event-stream")

    docs = await retriever.retrieve(user_message)

    if not docs:
        # Use customer-friendly fallback instead of error
        async def fallback_generator():
            for word in CUSTOMER_FRIENDLY_FALLBACK.split():
                yield f"data: {json.dumps({'type': 'content', 'content': word + ' '})}\n\n"
            yield "data: [DONE]\n\n"
        return StreamingResponse(fallback_generator(), media_type="text/event-stream")

    context = _build_context(docs)
    citations = _build_citations(docs)

    return StreamingResponse(
        llm_service.stream_response(user_message, context, citations, body.conversation_id),
        media_type="text/event-stream",
    )


@router.post("/ingest")
async def ingest(request: Request):
    crawler = request.app.state.crawler_service
    retriever = request.app.state.retriever

    try:
        result = await crawler.crawl()
        pages = result["pages"]
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

        import json as json_mod
        raw_path = os.path.join(settings.chroma_db_dir, "..", "data", "raw")
        processed_path = os.path.join(settings.chroma_db_dir, "..", "data", "processed")
        os.makedirs(raw_path, exist_ok=True)
        os.makedirs(processed_path, exist_ok=True)

        with open(os.path.join(raw_path, "raw_content.json"), "w", encoding="utf-8") as f:
            json_mod.dump(raw_content, f, indent=2, ensure_ascii=False)
        with open(os.path.join(processed_path, "chunks.json"), "w", encoding="utf-8") as f:
            json_mod.dump(chunks, f, indent=2, ensure_ascii=False)

        await retriever.index_chunks(chunks)

        return IngestionResponse(
            status="success",
            pages_crawled=pages,
            chunks_created=len(chunks),
            message=f"Crawled {pages} pages, created {len(chunks)} chunks, and indexed vectors.",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _build_context(docs) -> str:
    context_parts = []
    total_chars = 0
    for doc in docs:
        text = doc.get("text", doc.get("content", ""))
        source = doc.get("url", doc.get("source", "unknown"))
        entry = f"[Source: {source}]\n{text}\n"
        if total_chars + len(entry) > settings.max_context_chars:
            remaining = settings.max_context_chars - total_chars
            if remaining > 100:
                context_parts.append(entry[:remaining])
            break
        context_parts.append(entry)
        total_chars += len(entry)
    return "\n---\n".join(context_parts)


def _build_citations(docs) -> list:
    seen = set()
    citations = []
    for doc in docs:
        url = doc.get("url", doc.get("source", ""))
        if url and url not in seen:
            seen.add(url)
            citations.append({"url": url, "title": doc.get("title", "Flashoot Page")})
    return citations


async def _stream_error(message: str):
    data = json.dumps({"type": "error", "content": message})
    yield f"data: {data}\n\n"
    yield "data: [DONE]\n\n"
