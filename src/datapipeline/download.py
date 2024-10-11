import os
from google.cloud import storage
from tqdm import tqdm

#! Under construction!

BUCKET_NAME = 'ac215-reddit-finance-data'
GCS_FILES = {
    'train.jsonl': 'reddit-processed/train.jsonl',
    'validation.jsonl': 'reddit-processed/validation.jsonl',
    'top.jsonl': 'reddit-raw/top.jsonl',
}
LOCAL_DIR = 'datasets/'

def download_from_gcs(bucket_name, source_blob_name, destination_file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    
    try:
        file_size = blob.size
        if file_size is None:
            raise ValueError(f"Blob {source_blob_name} not found in bucket {bucket_name}")

        with open(destination_file_name, "wb") as file_obj:
            with tqdm(total=file_size, unit="B", unit_scale=True, desc=destination_file_name) as pbar:
                chunk_size = 1024 * 1024
                start = 0

                while start < file_size:
                    end = min(start + chunk_size, file_size)
                    chunk = blob.download_as_bytes(start=start, end=end-1)
                    file_obj.write(chunk)
                    pbar.update(len(chunk))
                    start = end

        print(f"Downloaded {source_blob_name} to {destination_file_name}.")

    except Exception as e:
        print(f"Failed to download {source_blob_name}: {str(e)}")

def is_directory_empty(directory):
    return not any(os.scandir(directory))

def download_gcs_files_if_needed():
    if not os.path.exists(LOCAL_DIR):
        os.makedirs(LOCAL_DIR)
    
    if is_directory_empty(LOCAL_DIR):
        print("Dataset directory is empty. Downloading files from GCS...")
        for local_file, gcs_path in GCS_FILES.items():
            try:
                download_from_gcs(BUCKET_NAME, gcs_path, os.path.join(LOCAL_DIR, local_file))
            except Exception as e:
                print(f"Error downloading {gcs_path}: {e}")
        print("Download completed.")
    else:
        print("Dataset directory is not empty. No need to download.")

if __name__ == "__main__":
    download_gcs_files_if_needed()
