#!/usr/bin/env bash
set -euo pipefail

if [ ! -d ".venv" ]; then
  python -m venv .venv
fi

source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload
