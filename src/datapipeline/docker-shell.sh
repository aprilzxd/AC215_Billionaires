docker run --rm -ti \
  -v "$(pwd)/../../../secrets:/secrets" \
  -v "$(pwd)/../data:/app/data" \
  -e GOOGLE_APPLICATION_CREDENTIALS="/secrets/data-service-account.json" \
  datapipeline:latest