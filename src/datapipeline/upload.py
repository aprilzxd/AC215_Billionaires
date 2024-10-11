from google.cloud import storage
from tqdm import tqdm
import os
import time

storage_client = storage.Client()

def upload_to_gcs(bucket_name, source_file_name, destination_blob_name, chunk_size=1024*1024):
    file_size = os.path.getsize(source_file_name)
    
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    
    with open(source_file_name, 'rb') as file_obj, tqdm(total=file_size, unit='B', unit_scale=True, desc=source_file_name) as pbar:
        while True:
            chunk = file_obj.read(chunk_size)
            if not chunk:
                break
            try:
                blob.upload_from_file(file_obj, size=len(chunk), rewind=True)
            except:
                time.sleep(5)
                blob.upload_from_file(file_obj, size=len(chunk), rewind=True)
            pbar.update(len(chunk))
            

bucket_name = 'ac215-reddit-finance-data'

print("start uploading")
upload_to_gcs(
    bucket_name=bucket_name,
    source_file_name='dataset/top.jsonl',
    destination_blob_name='reddit-raw/top.jsonl'
)
print("finish raw upload")

upload_to_gcs(
    bucket_name=bucket_name,
    source_file_name='dataset/train.jsonl',
    destination_blob_name='reddit-processed/train/train.jsonl'
)
print("finish train upload")

upload_to_gcs(
    bucket_name=bucket_name,
    source_file_name='dataset/validation.jsonl',
    destination_blob_name='reddit-processed/validation/validation.jsonl'
)
print("finish validation upload")
print("finish the process")


