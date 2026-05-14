import os
from typing import Optional, List


class Settings:
    groq_api_key: Optional[str] = os.getenv("GROQ_API_KEY")
    gemini_api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
    mistral_api_key: Optional[str] = os.getenv("MISTRAL_API_KEY")
    openrouter_api_key: Optional[str] = os.getenv("OPENROUTER_API_KEY")
    nvidia_api_key: Optional[str] = os.getenv("NVIDIA_API_KEY")

    llm_provider: str = os.getenv("LLM_PROVIDER", "groq")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    vector_db: str = os.getenv("VECTOR_DB", "chroma")
    chroma_db_dir: str = os.getenv("CHROMA_DB_DIR", "./vectordb")

    allowed_origin: str = os.getenv("ALLOWED_ORIGIN", "*")
    top_k_results: int = int(os.getenv("TOP_K_RESULTS", "4"))
    max_context_chars: int = int(os.getenv("MAX_CONTEXT_CHARS", "4000"))
    enable_provider_fallback: bool = os.getenv("ENABLE_PROVIDER_FALLBACK", "true").lower() == "true"

    chunk_size: int = int(os.getenv("CHUNK_SIZE", "800"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "120"))

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    provider_priority: List[str] = [
        os.getenv("LLM_PROVIDER", "groq"),
        "gemini",
        "mistral",
        "openrouter",
        "nvidia",
        "ollama",
        "fallback",
    ]

    @property
    def provider_api_keys(self) -> dict:
        return {
            "groq": self.groq_api_key,
            "gemini": self.gemini_api_key,
            "mistral": self.mistral_api_key,
            "openrouter": self.openrouter_api_key,
            "nvidia": self.nvidia_api_key,
        }


settings = Settings()
