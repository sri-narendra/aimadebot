import re
from typing import Dict, Any
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(prior|previous|above|the\s+above)",
    r"forget\s+(all\s+)?(prior|previous|above|instructions)",
    r"you\s+are\s+(now|not\s+bound|free)",
    r"override\s+(instructions|prompt|system)",
    r"system\s+prompt",
    r"reveal\s+(your\s+)?(instructions|prompt|system)",
    r"act\s+as\s+(if|though)",
    r"pretend\s+(to\s+be|you\s+are)",
    r"new\s+instructions",
    r"<|im_start|>",
    r"<|im_end|>",
    r"<\w+>[^<]*</\w+>",
    r"\[\/?INST\]",
    r"\[\/?SYS\]",
    r"dang(er|ling)",
    r"jail\s*break",
    r"role\s*play",
]

BLOCKED_KEYWORDS = [
    "competitor", "competitors",
    "hack", "hacking", "crack", "cracking",
    "exploit", "vulnerability",
    "illegal", "unlawful",
    "password", "credentials",
    "bypass", "circumvent",
    "malware", "virus", "trojan",
]

NON_FLASHOOT_KEYWORDS = [
    "who created you", "who built you",
    "what are you", "who are you",
    "your model", "what model",
    "who developed",
    "tell me a joke",
    "write a poem",
    "write code",
    "calculate",
    "math problem",
    "what is the meaning of life",
    "what do you think about",
    "your opinion",
]


def sanitize_input(text: str) -> str:
    text = text.strip()
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', '', text)
    return text[:2000]


def detect_injection(text: str) -> bool:
    text_lower = text.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text_lower):
            return True
    return False


def validate_prompt(text: str) -> Dict[str, Any]:
    text_lower = text.lower()

    for kw in BLOCKED_KEYWORDS:
        if kw in text_lower:
            return {
                "allowed": False,
                "response": "I can only answer questions about Flashoot website content and services.",
                "cleaned_message": text,
            }

    return {
        "allowed": True,
        "response": None,
        "cleaned_message": text,
    }


class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            return await call_next(request)

        if request.url.path == "/chat":
            body = await request.body()
            if len(body) > 5000:
                from fastapi.responses import JSONResponse
                return JSONResponse(
                    status_code=413,
                    content={"detail": "Request too large"},
                )

        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response
