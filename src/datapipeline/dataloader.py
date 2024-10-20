import os
import argparse
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
    parser = argparse.ArgumentParser(description="Download raw or process data (reddit_500, reddit_1000, etc.) from GCS.")
    parser.add_argument("dir", help="Specify the folder: 'raw' or 'reddit_500', 'reddit_1000', etc.")
    args = parser.parse_args()

    LOCAL_DIR = "dataset"
    bucket_name = "finance_215"
    dir = args.dir

    if dir == 'raw':
        download_file_from_gcs(
            bucket_name=bucket_name,
            source_blob_name=f"{dir}/top.jsonl",
            destination_file_name=f"{LOCAL_DIR}/top.jsonl",
        )
    else:
        download_file_from_gcs(
            bucket_name=bucket_name,
            source_blob_name=f"{dir}/train.jsonl",
            destination_file_name=f"{LOCAL_DIR}/train.jsonl",
        )
        download_file_from_gcs(
            bucket_name=bucket_name,
            source_blob_name=f"{dir}/test.jsonl",
            destination_file_name=f"{LOCAL_DIR}/test.jsonl",
        )
