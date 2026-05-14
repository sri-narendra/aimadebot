#!/bin/bash
# Crawl Flashoot website and ingest content
# Usage: ./scripts/crawl.sh [backend_url]

BACKEND_URL="${1:-http://localhost:8000}"

echo "Starting Flashoot website crawl..."
echo "Backend URL: $BACKEND_URL"

curl -X POST "$BACKEND_URL/ingest" \
  -H "Content-Type: application/json" \
  -d '{}'

echo -e "\nCrawl complete."
