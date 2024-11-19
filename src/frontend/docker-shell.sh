docker build -t agents -f Dockerfile .

docker run --rm --network my-network --name streamlit-container -it -p 8501:8501 agents
