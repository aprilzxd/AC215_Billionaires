docker build -t agents -f Dockerfile .

docker run --rm -it -p 8501:8501 agents
