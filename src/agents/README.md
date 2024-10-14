docker build -t agents-image .

docker run -it --name agents-container -e OPENAI_API_KEY=your_openai_api_key -p 8501:8501 agents-image /bin/bash

pipenv run streamlit run finance_assistant.py --server.address 0.0.0.0

http://localhost:8501
