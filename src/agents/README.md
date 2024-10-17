docker build -t agents .

docker run --rm -it -e OPENAI_API_KEY=your_openai_api_key -p 8501:8501 agents

pipenv run streamlit run finance_assistant.py --server.address 0.0.0.0

http://localhost:8501
