#! Under construction!
import os
from google.cloud import storage

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../secrets/llm-service-account.json"

def download_file_from_gcs(bucket_name, source_blob_name, destination_file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(
        f"Downloaded {source_blob_name} from bucket {bucket_name} to {destination_file_name}."
    )

if __name__ == "__main__":
    LOCAL_DIR = "dataset"
    ftype = "train" # or "test"
    bucket_name = "finance_215"
    source_blob_name = f"reddit_500/{ftype}.jsonl"
    if not os.path.exists(LOCAL_DIR):
        os.makedirs(LOCAL_DIR)
    destination_file_name = f"{LOCAL_DIR}/{ftype}.jsonl"
    download_file_from_gcs(
        bucket_name=bucket_name,
        source_blob_name=source_blob_name,
        destination_file_name=destination_file_name,
    )
