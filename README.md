# Flashoot AI Chatbot

A production-ready, lightweight AI chatbot for [Flashoot.com](https://www.flashoot.com/) using Retrieval-Augmented Generation (RAG). Answers questions exclusively about Flashoot products, services, and website content with source citations.

## Architecture

```
User ──→ index.html (GitHub/Cloudflare Pages)
              │
              │ POST /chat (SSE streaming)
              ▼
        FastAPI Backend (Render.com)
              │
        ┌─────┼─────────┐
        ▼     ▼         ▼
     Crawler  RAG     LLM Provider
     (scrape) │      (multi-provider)
              ▼
         Vector DB
         (ChromaDB)
```

### Key Design Decisions

- **RAG over fine-tuning**: Cheaper, easier maintenance, works with changing website content
- **Multi-provider LLM**: Groq, Gemini, Mistral, OpenRouter, NVIDIA, Ollama, or no-API fallback
- **No frontend build step**: Single `index.html`, works directly on static hosts
- **Dockerized backend**: Ready for Render free tier

## Project Structure

```
/
├── index.html                 # Frontend (single file)
├── backend/
│   ├── main.py                # FastAPI entry point
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile             # Container definition
│   ├── render.yaml            # Render.com config
│   ├── .env.example           # Environment variables template
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py          # Settings management
│   │   └── api.py             # API endpoints
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── embeddings.py      # Sentence transformer embeddings
│   │   └── retriever.py       # Vector DB retrieval
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm_service.py     # Multi-provider LLM orchestration
│   │   └── crawler.py         # Website crawler
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── security.py        # Input sanitization & injection defense
│   │   └── rate_limiter.py    # Rate limiting middleware
│   ├── data/
│   │   ├── raw/               # Crawled raw content
│   │   └── processed/         # Chunked content
│   └── vectordb/              # Persistent vector database
├── scripts/
│   ├── crawl.sh               # Crawl trigger script
│   ├── crawl.ps1              # Windows crawl script
│   └── start.sh               # Local dev start script
└── README.md
```

## Setup

### 1. Clone and Install Backend

```bash
cd backend
pip install -r requirements.txt
playwright install chromium
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

Minimum: set `GROQ_API_KEY` (free at console.groq.com). The system works with just one provider.

### 3. Run Locally

```bash
uvicorn main:app --reload --port 8000
```

### 4. Ingest Flashoot Content

```bash
curl -X POST http://localhost:8000/ingest
```

This crawls flashoot.com, chunks content, and builds the vector index.

### 5. Open Frontend

Open `index.html` in any browser or serve it:

```bash
python -m http.server 8080
# Then open http://localhost:8080
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Backend status and config |
| `/sources` | GET | List indexed sources |
| `/chat` | POST | Ask a question (SSE streaming) |
| `/ingest` | POST | Crawl website and index content |

## Deployment

### Backend → Render.com

1. Push to GitHub
2. In Render Dashboard: New + → Web Service
3. Connect repo, set:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python -m playwright install chromium --with-deps`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables (see `.env.example`)
5. Add a disk mount at `/var/data` (1 GB) for vector DB persistence
6. Deploy

### Frontend → GitHub Pages

1. Push `index.html` to a GitHub repo
2. Settings → Pages → Source: GitHub Actions (or deploy from branch)
3. Or just use `npx gh-pages -d .`

### Frontend → Cloudflare Pages

1. Log into Cloudflare Dashboard → Pages
2. Create a new project → connect your repo
3. Build settings: leave blank (no build step)
4. Deploy

### Update Backend URL

In `index.html`, change the `API_URL` constant:

```js
const CONFIG = {
  API_URL: 'https://your-app.onrender.com',
};
```

## LLM Providers

Set `LLM_PROVIDER` in environment to one of:

| Provider | Env Var | Model | Cost |
|----------|---------|-------|------|
| groq | `GROQ_API_KEY` | llama-3.1-8b-instant | Free tier available |
| gemini | `GEMINI_API_KEY` | gemini-1.5-flash | Free tier available |
| mistral | `MISTRAL_API_KEY` | mistral-small-latest | Pay-as-you-go |
| openrouter | `OPENROUTER_API_KEY` | gemma-2-9b-it (free) | Free options |
| nvidia | `NVIDIA_API_KEY` | llama3-8b-instruct | Free tier |
| ollama | OLLAMA_BASE_URL | llama3 (local) | Free (local) |
| fallback | none | Extractive QA | Free (no API) |

### Provider Fallback Chain

If `ENABLE_PROVIDER_FALLBACK=true`, on failure the system tries:
`primary → gemini → mistral → openrouter → nvidia → ollama → fallback (extractive QA)`

## Rate Limiting & Cost Optimization

- **Token economy**: `TOP_K_RESULTS=4` keeps context small. `MAX_CONTEXT_CHARS=4000` limits LLM input.
- **Embedding cache**: Repeated queries use cached embeddings.
- **Retrieval cache**: Same query within session hits cache.
- **Rate limiting**: 20 requests/minute per IP (configurable).
- **Provider fallback**: If one provider rate-limits, the next in chain is tried automatically.
- **Cooldown**: 2-second backoff on rate-limit errors.

## Security

- **Prompt injection defense**: Blocks jailbreak patterns, instruction overrides
- **Content restriction**: Only answers about Flashoot content
- **Input sanitization**: Strips HTML, control characters, limits length
- **CORS**: Configurable allowed origins
- **Rate limiting**: Per-IP request throttling

## No-API Fallback Mode

When no API keys are configured (`LLM_PROVIDER=fallback`), the system uses extractive QA:
- Retrieves relevant chunks from the vector DB
- Scores sentences by keyword overlap with the query
- Returns top matching sentences directly
- Still provides source citations

This means the chatbot partially works even with zero API cost.

## Performance Notes

- Embedding model runs on CPU (~500ms per query)
- ChromaDB persists to disk (survives restarts on Render)
- Streaming responses start in ~1-2 seconds with Groq
- Total RAM usage: ~400-600 MB (fits Render free tier)
- Cold start: ~15-30 seconds on Render free tier (expected)

## Troubleshooting

**Q: Backend returns 503 on first request**
A: Render free tier spins down after inactivity. Wait 30s and retry.

**Q: "No relevant information found"**
A: Run the `/ingest` endpoint to crawl and index Flashoot content.

**Q: Embedding model fails to load**
A: Ensure `sentence-transformers` is installed. First load downloads the model (~90MB).

**Q: ChromaDB errors**
A: Delete the `vectordb/` directory and re-run `/ingest`.

**Q: CORS errors in browser**
A: Set `ALLOWED_ORIGIN` to your frontend domain, or `*` during development.

## Scaling

- **More content**: Increase `MAX_PAGES` in crawler
- **Better retrieval**: Increase `TOP_K_RESULTS` (more tokens = higher cost)
- **Faster responses**: Switch to Groq (fastest inference)
- **Larger vector DB**: Increase disk size on Render
- **Production**: Add Redis cache, PostgreSQL for chat history
