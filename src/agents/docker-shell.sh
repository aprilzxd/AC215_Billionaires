docker build -t agents -f Dockerfile .

docker run --rm -it -e OPENAI_API_KEY=your_openai_api_key -p 8501:8501 agents
