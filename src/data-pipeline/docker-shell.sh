docker build -t datapipeline -f Dockerfile .

docker run --rm -ti \
  -v "$(pwd)/../../../secrets:/secrets" \
  -v "$(pwd)/../../dataset:/app/dataset" \
  -e GOOGLE_APPLICATION_CREDENTIALS="/secrets/llm-service-account.json" \
  datapipeline:latest
