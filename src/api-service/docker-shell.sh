#!/bin/bash

export SECRETS_DIR=$(realpath $(pwd)/../../../secrets/openai_key)

docker run -p 8001:8001 \
  -v "$SECRETS_DIR":/run/secrets/openai_key:ro \
  -e OPENAI_API_KEY_FILE=/run/secrets/openai_key \
  api-service
