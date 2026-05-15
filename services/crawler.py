import os
import re
import asyncio
from typing import Dict, List, Set, Optional
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup


TARGET_URL = "https://www.flashoot.com/"
EXTRA_PAGES = [
    "https://www.flashoot.com/discover",
    "https://www.flashoot.com/partner", 
    "https://www.flashoot.com/journey",
]
MAX_PAGES = 50
TIMEOUT = 15


class CrawlerService:
    def __init__(self):
        self.visited: Set[str] = set()
        self.results: Dict[str, str] = {}

    async def crawl(self) -> dict:
        self.visited.clear()
        self.results.clear()

        # Start from all key pages
        all_start_urls = [TARGET_URL] + EXTRA_PAGES
        
        try:
            for start_url in all_start_urls:
                if len(self.visited) >= MAX_PAGES:
                    break
                await self._crawl_with_httpx(start_url)
        except Exception as e:
            try:
                for start_url in all_start_urls:
                    if len(self.visited) >= MAX_PAGES:
                        break
                    await self._crawl_with_playwright(start_url)
            except Exception as pe:
                raise RuntimeError(f"Crawling failed: httpx error: {e}, playwright error: {pe}")

        return {
            "pages": len(self.visited),
            "content": self.results,
        }

    async def _crawl_with_playwright(self, start_url: str):
        try:
            from playwright.async_api import async_playwright
        except ImportError:
            raise ImportError("Playwright not installed")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="FlashootBot/1.0 (RAG Crawler)",
                viewport={"width": 1280, "height": 720},
            )
            page = await context.new_page()

            urls_to_visit = [start_url]
            while urls_to_visit and len(self.visited) < MAX_PAGES:
                url = urls_to_visit.pop(0)
                if url in self.visited:
                    continue

                try:
                    await page.goto(url, wait_until="domcontentloaded", timeout=TIMEOUT * 1000)
                    self.visited.add(url)

                    content = await page.content()
                    cleaned = self._clean_html(content, url)
                    if cleaned.strip():
                        self.results[url] = cleaned

                    links = await page.evaluate("""
                        () => Array.from(document.querySelectorAll('a[href]'))
                            .map(a => a.href)
                    """)

                    for link in links:
                        normalized = self._normalize_url(link)
                        if normalized and normalized not in self.visited:
                            urls_to_visit.append(normalized)

                except Exception as e:
                    print(f"Failed to crawl {url}: {e}")
                    self.visited.add(url)
                    continue

            await browser.close()

    async def _crawl_with_httpx(self, start_url: str):
        import httpx

        async with httpx.AsyncClient(
            timeout=TIMEOUT,
            follow_redirects=True,
            headers={"User-Agent": "FlashootBot/1.0 (RAG Crawler)"},
        ) as client:

            urls_to_visit = [start_url]
            while urls_to_visit and len(self.visited) < MAX_PAGES:
                url = urls_to_visit.pop(0)
                if url in self.visited:
                    continue

                try:
                    resp = await client.get(url)
                    self.visited.add(url)

                    if resp.status_code == 200 and "text/html" in resp.headers.get("content-type", ""):
                        cleaned = self._clean_html(resp.text, url)
                        if cleaned.strip():
                            self.results[url] = cleaned

                        soup = BeautifulSoup(resp.text, "html.parser")
                        for a in soup.find_all("a", href=True):
                            link = urljoin(url, a["href"])
                            normalized = self._normalize_url(link)
                            if normalized and normalized not in self.visited:
                                urls_to_visit.append(normalized)

                except Exception as e:
                    print(f"Failed to crawl {url}: {e}")
                    self.visited.add(url)
                    continue

    def _clean_html(self, html: str, url: str) -> str:
        soup = BeautifulSoup(html, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header", "noscript",
                         "iframe", "svg", "form", "button", "input", "select",
                         "textarea", "aside", "menu", "menuitem"]):
            tag.decompose()

        for tag in soup.find_all(class_=lambda c: c and any(
            x in (c.lower() if c else "") for x in ["nav", "footer", "header", "sidebar",
                                                      "menu", "cookie", "popup", "modal",
                                                      "overlay", "banner", "social"])):
            tag.decompose()

        for tag in soup.find_all(id=lambda i: i and any(
            x in (i.lower() if i else "") for x in ["nav", "footer", "header", "sidebar",
                                                      "menu", "cookie", "popup"])):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)

        lines = []
        for line in text.split("\n"):
            line = line.strip()
            if not line:
                continue
            if len(line) < 15 and any(
                kw in line.lower() for kw in ["cookie", "privacy", "terms", "all rights",
                                               "©", "subscribe", "follow", "share"]
            ):
                continue
            lines.append(line)

        text = "\n".join(lines)
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[ \t]+', ' ', text)

        return text.strip()

    def _normalize_url(self, url: str) -> Optional[str]:
        parsed = urlparse(url)

        if parsed.netloc and "flashoot.com" not in parsed.netloc:
            return None
        if parsed.scheme not in ("http", "https"):
            return None

        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path.rstrip('/')}"

        if not parsed.netloc:
            return None

        if any(ext in normalized for ext in [".pdf", ".jpg", ".png", ".gif", ".mp4",
                                               ".zip", ".xml", ".rss", ".json",
                                               ".css", ".js", ".svg", ".ico", ".webp"]):
            return None

        if any(skip in normalized for skip in ["#", "mailto:", "tel:", "javascript:",
                                                 "wp-", "/tag/", "/category/",
                                                 "/feed/", "/comment"]):
            return None

        # Accept any flashoot.com URL, not just exact matches
        if "flashoot.com" in normalized:
            return normalized

        return None
