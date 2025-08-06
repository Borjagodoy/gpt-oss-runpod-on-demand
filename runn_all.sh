#!/bin/bash

# Load environment variables
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Start the proxy (FastAPI) in the background
echo "[RunAll] Starting proxy on port 8001..."
uvicorn proxy.main:app --host 0.0.0.0 --port 8001 &

# Start the auto-shutdown script in the background
echo "[RunAll] Starting auto-shutdown watcher..."
python3 scripts/auto_shutdown.py &

# Wait for both processes to run indefinitely
wait
