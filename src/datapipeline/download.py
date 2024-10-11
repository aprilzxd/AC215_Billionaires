#! Under construction!
import os
from google.cloud import storage

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../secrets/data-service-account.json"


def download_file_from_gcs(bucket_name, source_blob_name, destination_file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(
        f"Downloaded {source_blob_name} from bucket {bucket_name} to {destination_file_name}."
    )


if __name__ == "__main__":
    LOCAL_DIR = "datasets"
    bucket_name = "ac215-reddit-finance-data"
    source_blob_name = "reddit-processed/train/reddit_1k.jsonl"
    if not os.path.exists(LOCAL_DIR):
        os.makedirs(LOCAL_DIR)
    destination_file_name = f"{LOCAL_DIR}/hi.jsonl"
    download_file_from_gcs(
        bucket_name=bucket_name,
        source_blob_name=source_blob_name,
        destination_file_name=destination_file_name,
    )
