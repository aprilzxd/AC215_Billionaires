import os
import argparse
from google.cloud import storage
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig

# Setup
GCP_PROJECT = os.environ["GCP_PROJECT"]
GCP_LOCATION = "us-central1"
# GENERATIVE_SOURCE_MODEL = "gemini-1.5-flash-002"
generation_config = {
    "max_output_tokens": 3000,
    "temperature": 0.75,
    "top_p": 0.95,
}

vertexai.init(project=GCP_PROJECT, location=GCP_LOCATION)

def chat(query):
    print("chat()")
    # MODEL_ENDPOINT = "projects/738060168305/locations/us-central1/endpoints/4117575388509503488"  # Finance-215-v1 (500 data, 1 epoch)
    # MODEL_ENDPOINT = "projects/738060168305/locations/us-central1/endpoints/2997797562410336256"  # Finance-215-v2 (1000 data, 3 epochs)
    MODEL_ENDPOINT = "projects/738060168305/locations/us-central1/endpoints/5609885346285223936"  # Finance-215-v2 (1000 data, 2 epochs)
    generative_model = GenerativeModel(MODEL_ENDPOINT)

    print("query: ", query)
    response = generative_model.generate_content(
        [query],
        generation_config=generation_config,
        stream=False,
    )
    generated_text = response.text
    print("Fine-tuned LLM Response:", generated_text)

def main(args=None):
    default_query="Give me some recommendations on Nvidia's stock. I am student, and I don't have so much money."
    query = args.query or default_query
    chat(query)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI for querying the model")

    parser.add_argument(
        "--query",
        type=str,
        help="The query to send to the model",
    )

    args = parser.parse_args()
    main(args)
