#!/bin/bash

set -e

export BASE_DIR=$(pwd)
export PERSISTENT_DIR=$(pwd)/../persistent-folder/
export SECRETS_DIR=$(pwd)/../../../secrets/
export GCP_PROJECT="marine-bruin-434717-k2"
export GOOGLE_APPLICATION_CREDENTIALS="/secrets/data-service-account.json"
export IMAGE_NAME="data-preprocess"

docker network inspect llm-rag-network >/dev/null 2>&1 || docker network create llm-rag-network

docker build -t $IMAGE_NAME -f Dockerfile .

docker-compose run --rm --service-ports $IMAGE_NAME