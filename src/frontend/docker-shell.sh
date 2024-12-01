docker build -t frontend -f Dockerfile .

docker run --rm --network my-network --name frontend-container -it -p 8501:8501 frontend
