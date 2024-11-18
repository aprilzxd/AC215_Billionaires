export SECRETS_DIR=$(pwd)/../../../secrets/
export OPENAI_API_KEY=$(cat ${SECRETS_DIR}/openai_key.txt)

docker build -t api-service -f Dockerfile .

docker run --rm --network my-network --name api-container -p 8001:8001 \
  -v "$SECRETS_DIR":/run/secrets/openai_key:ro \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  api-service
