from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from boto3 import client
import os
from dotenv import load_dotenv
import threading
import queue

from typing import List

load_dotenv()


AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_ACCESS_KEY_VALUE = os.getenv('AWS_ACCESS_KEY_VALUE')
S3_BUCKET = 'meayudai-files'
S3_REGION = 'oregon'
# Directory to save uploaded files
UPLOAD_DIR = "data"

os.makedirs(UPLOAD_DIR, exist_ok=True)

AWS_CLIENT = client(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_ACCESS_KEY_VALUE, service_name='s3')

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    buckets = AWS_CLIENT.list_buckets()
    AWS_CLIENT.upload_file(f'data/prueba lourdes completa.pdf', S3_BUCKET, f'test/test5.pdf')
    return {"message": f'File should have been uploaded to bucket: {S3_BUCKET}'}


@app.post("/pauta/")
async def upload_file(file: UploadFile = File(...)):
    AWS_CLIENT.upload_fileobj(
            Fileobj=file.file,  # Streamed file-like object
            Bucket=S3_BUCKET,
            Key=f'data/{file.filename}',
            ExtraArgs={"ContentType": file.content_type}  # Optional: preserve MIME type
        )

    # Construct a public file URL (if your S3 bucket is public)
    file_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{file.filename}"

    return {
        "filename": file.filename,
        "url": file_url,
        "message": "File uploaded successfully to S3!"
    }


# Worker function
def upload_worker(file_queue):
    while True:
        file = file_queue.get()
        if file is None:  # Exit signal
            break
        try:
            AWS_CLIENT.upload_fileobj(
                Fileobj=file.file,  # Streamed file-like object
                Bucket=S3_BUCKET,
                Key=f"data/{file.filename}",
                ExtraArgs={"ContentType": file.content_type}  # Preserve MIME type
            )
            print(f"Uploaded: {file.filename}")
        except Exception as e:
            print(f"Error uploading {file.filename}: {e}")
        finally:
            file_queue.task_done()

# FastAPI endpoint for file upload
@app.post("/prueba/")
async def upload_file(files: List[UploadFile] = File(...)):
    file_queue = queue.Queue()
    NUM_WORKERS = 4  # Number of worker threads
    threads = []

    # Start worker threads dynamically
    for _ in range(NUM_WORKERS):
        t = threading.Thread(target=upload_worker, args=(file_queue,), daemon=True)
        t.start()
        threads.append(t)

    # Add files to the queue (producer)
    file_urls = []
    for file in files:
        file_queue.put(file)
        file_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/data/{file.filename}"
        file_urls.append(file_url)
    
    # Wait for all tasks in the queue to be processed
    file_queue.join()

    # Stop the worker threads
    for _ in range(NUM_WORKERS):
        file_queue.put(None)  # Signal workers to exit
    for t in threads:
        t.join()

    return {
        "message": "Files uploaded successfully to S3!",
        "files": file_urls
    }