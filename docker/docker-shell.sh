#!/bin/bash
set -e

export SECRETS_DIR=$(pwd)/../secrets/
if [ ! -f "${SECRETS_DIR}/openai_key.txt" ]; then
  echo "Error: openai_key.txt not found in ${SECRETS_DIR}!"
  exit 1
fi

export OPENAI_API_KEY=$(cat ${SECRETS_DIR}/openai_key.txt)

docker-compose up --build -d

echo "Containers are starting..."
echo "OPENAI_API_KEY is loaded from ${SECRETS_DIR}/openai_key.txt"