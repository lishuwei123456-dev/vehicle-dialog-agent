#!/usr/bin/env bash
set -euo pipefail

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export APP_ENV="${APP_ENV:-autodl}"
export STATE_BACKEND="${STATE_BACKEND:-memory}"
export WEATHER_PROVIDER="${WEATHER_PROVIDER:-demo}"

uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8080}"
