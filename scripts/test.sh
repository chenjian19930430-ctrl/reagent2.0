#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
echo "Running tests..."
python3 -m pytest customer-profile/test_enricher.py -v
