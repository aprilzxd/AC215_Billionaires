docker build -t frontend -f Dockerfile .

docker run --rm --network my-network --name frontend -it -p 8501:8501 frontend
