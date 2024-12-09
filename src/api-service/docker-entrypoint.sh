#!/bin/bash
set -e
if [ -z "$PORT" ]; then
  PORT=8001
fi
exec uvicorn api.main:app --host 0.0.0.0 --port $PORT
