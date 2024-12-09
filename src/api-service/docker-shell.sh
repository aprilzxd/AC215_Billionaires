export SECRETS_DIR=$(pwd)/../../../secrets/
export OPENAI_API_KEY=$(cat ${SECRETS_DIR}/openai_key.txt)

if ! docker network ls | grep -q "my-network"; then
  docker network create my-network
fi

docker build -t api-service -f Dockerfile .

docker run --rm --network my-network --name api-service -p 8001:8001 \
  -v "$SECRETS_DIR":/run/secrets/openai_key:ro \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  api-service