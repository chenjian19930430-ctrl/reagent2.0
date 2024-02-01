#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
echo "Starting ReAgent API server..."
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
