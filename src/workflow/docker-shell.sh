#!/bin/bash

# set -e

export IMAGE_NAME="billionairs-workflow"
export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../../secrets/
export GCP_PROJECT="unified-canyon-436117-q9"
export GCS_BUCKET_NAME="finance_215-tut"
export GCS_SERVICE_ACCOUNT="llm-service-account@unified-canyon-436117-q9.iam.gserviceaccount.com"
export GCP_SERVICE_ACCOUNT="llm-service-account@unified-canyon-436117-q9.iam.gserviceaccount.com"
export GCP_REGION="us-central1"
export LOCATION="us-central1"
# export GCS_PACKAGE_URI="gs://cheese-app-trainer-code"




# Build the image based on the Dockerfile
docker build -t $IMAGE_NAME -f Dockerfile .
# docker build -t $IMAGE_NAME --platform=linux/amd64 -f Dockerfile .


# Run Container
docker run --rm --name $IMAGE_NAME -ti \
-v /var/run/docker.sock:/var/run/docker.sock \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/secrets \
-e GOOGLE_APPLICATION_CREDENTIALS=/secrets/llm-service-account.json \
-e GCP_PROJECT=$GCP_PROJECT \
-e GCS_BUCKET_NAME=$GCS_BUCKET_NAME \
-e GCS_SERVICE_ACCOUNT=$GCS_SERVICE_ACCOUNT \
$IMAGE_NAME
# -e GCP_REGION=$GCP_REGION \
# -e GCS_PACKAGE_URI=$GCS_PACKAGE_URI \


