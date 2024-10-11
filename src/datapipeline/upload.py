from google.cloud import storage

storage_client = storage.Client()


def upload_to_gcs(
    bucket_name,
    source_file_path,
    destination_blob_name,
    credentials_file="../secrets/data-service-account.json",
):
    storage_client = storage.Client.from_service_account_json(credentials_file)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_path)
    print(
        f"File {source_file_path} uploaded to gs://{bucket_name}/{destination_blob_name}"
    )


bucket_name = "ac215-reddit-finance-data"

print("start uploading")
# upload_to_gcs(
#     bucket_name=bucket_name,
#     source_file_path="dataset/top.jsonl",
#     destination_blob_name="reddit-raw/top.jsonl",
# )

upload_to_gcs(
    bucket_name=bucket_name,
    source_file_path="dataset/reddit_1k.jsonl",
    destination_blob_name="reddit-processed/train/reddit_1k.jsonl",
)

upload_to_gcs(
    bucket_name=bucket_name,
    source_file_path="dataset/reddit_500.jsonl",
    destination_blob_name="reddit-processed/train/reddit_500.jsonl",
)
print("finish the process")
