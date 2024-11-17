# export SECRETS_DIR=$(pwd)/../../../secrets/
# export OPENAI_API_KEY=$(cat ${SECRETS_DIR}/openai_key.txt)

docker build -t agents -f Dockerfile .

# docker run --rm -it -p 8501:8501 agents




docker run --rm --network my-network --name streamlit-container -it -p 8501:8501 agents
