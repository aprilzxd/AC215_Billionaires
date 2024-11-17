export SECRETS_DIR=$(pwd)/../../../secrets/
export OPENAI_API_KEY=$(cat ${SECRETS_DIR}/openai_key.txt)

docker build -t agents -f Dockerfile .

docker run --rm -it -e OPENAI_API_KEY=$OPENAI_API_KEY -p 8501:8501 agents
