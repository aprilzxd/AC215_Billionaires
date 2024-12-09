docker build -t mamingyuan2001/billionaire-api-service:v12 --platform=linux/amd64/v2 -f Dockerfile .
docker push mamingyuan2001/billionaire-api-service:v12

docker build -t mamingyuan2001/billionaire-frontend:v12 --platform=linux/amd64/v2 -f Dockerfile .
docker push mamingyuan2001/billionaire-frontend:v12

gcloud container clusters create test-cluster --num-nodes 2 --zone us-east1-c --machine-type n2d-standard-2

