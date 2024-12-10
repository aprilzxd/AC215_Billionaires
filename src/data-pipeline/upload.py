import argparse
from google.cloud import storage

storage_client = storage.Client()

def upload_to_gcs(
    bucket_name,
    source_file_path,
    destination_blob_name,
    credentials_file="../secrets/llm-service-account.json",
):
    storage_client = storage.Client.from_service_account_json(credentials_file)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_path)
    print(
        f"File {source_file_path} uploaded to gs://{bucket_name}/{destination_blob_name}"
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload processed data to GCS folder (reddit_500, reddit_1000, etc.).")
    parser.add_argument("dir", help="Specify the folder: 'raw' or 'reddit_500', 'reddit_1000', etc.")
    args = parser.parse_args()

    LOCAL_DIR = "dataset"
    bucket_name = "finance_215"
    dir = args.dir

    print("Uploading...")

    upload_to_gcs(
        bucket_name=bucket_name,
        source_file_path=f"{LOCAL_DIR}/train.jsonl",
        destination_blob_name=f"{dir}/train.jsonl",
    )

    upload_to_gcs(
        bucket_name=bucket_name,
        source_file_path=f"{LOCAL_DIR}/test.jsonl",
        destination_blob_name=f"{dir}/test.jsonl",
    )
