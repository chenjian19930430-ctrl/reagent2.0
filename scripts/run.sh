#!/bin/bash
# ReAgent — Development server startup script
set -euo pipefail

cd "$(dirname "$0")/.."

# Check Python environment
if ! command -v python3 &> /dev/null; then
    echo "❌ python3 not found"
    exit 1
fi

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

echo "🚀 Starting ReAgent v2.0.0..."
echo "   API docs: http://localhost:8000/docs"
echo "   Health:    http://localhost:8000/api/v1/health"
echo ""

python3 -m reagent.main
