export SECRETS_DIR=$(pwd)/../secrets/
export OPENAI_API_KEY=$(cat ${SECRETS_DIR}/openai_key.txt)

docker-compose -f docker-compose.yml build

docker-compose -f docker-compose.yml up -d