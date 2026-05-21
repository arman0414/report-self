#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

PORT="${PORT:-8013}"
HOST="${HOST:-127.0.0.1}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is required. Install it from https://www.python.org/downloads/ and run again."
  exit 1
fi

if [ ! -d .venv ]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

echo "Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "ReportSelf is starting at http://${HOST}:${PORT}"
echo "  UI:   http://127.0.0.1:${PORT}/"
echo "  API:  http://127.0.0.1:${PORT}/docs"
echo "Press Ctrl+C to stop."
echo ""

exec uvicorn app.main:app --reload --host "$HOST" --port "$PORT"
