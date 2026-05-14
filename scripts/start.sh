#!/bin/bash
# Start the Flashoot chatbot backend
# Usage: ./scripts/start.sh

echo "Starting Flashoot AI Chatbot Backend..."

# Check for .env file
if [ -f backend/.env ]; then
    echo "Loading environment from backend/.env"
    export $(grep -v '^#' backend/.env | xargs)
fi

cd backend || exit 1

echo "Installing dependencies..."
pip install -r requirements.txt -q

echo "Starting uvicorn server..."
uvicorn main:app --host 0.0.0.0 --port "${PORT:-8000}" --reload
