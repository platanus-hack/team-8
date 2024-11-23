# FastApi Imports
from fastapi import APIRouter, File, UploadFile, HTTPException

# Libraries Imports
import threading
import queue
import os
from boto3 import client
from typing import List
import json

# Local Imports
from .services import open_textract_json

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_ACCESS_KEY_VALUE = os.getenv('AWS_ACCESS_KEY_VALUE')
S3_BUCKET = 'meayudai-files'
S3_REGION = 'oregon'
# Directory to save uploaded files
UPLOAD_DIR = "data"

os.makedirs(UPLOAD_DIR, exist_ok=True)

AWS_S3_CLIENT = client(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_ACCESS_KEY_VALUE, service_name='s3')
AWS_ANSWER_PARSER_AGENT = client(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_ACCESS_KEY_VALUE, service_name='bedrock-agent-runtime', region_name='us-west-2')


TEXTRACT_CLIENT = client(
    'textract',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_ACCESS_KEY_VALUE,
    region_name='us-west-2'  # Cambia por la región correcta
)


api_router = APIRouter()


@api_router.get("/list_files/")
async def list_files():
    """
    List all files in the S3 bucket.
    
    Returns:
    - List of files in the S3 bucket.
    """
    try:
        # List all files in the S3 bucket
        files = AWS_S3_CLIENT.list_objects(Bucket=S3_BUCKET)
        files_list = [file['Key'] for file in files['Contents']]
        
        # Return the list of files
        return files_list
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@api_router.post("/analyze/")
async def analyze_file_s3(file_key: str):
    try:
        # Construct the S3 object URL
        s3_object_url = f"s3://{S3_BUCKET}/{file_key}"
        # Call AWS Textract to analyze the file in S3
        response = TEXTRACT_CLIENT.start_document_text_detection(
            DocumentLocation={
                'S3Object': {
                    'Bucket': S3_BUCKET,
                    'Name': file_key
                }
            }
        )
        # Get the JobId from the response
        job_id = response.get('JobId')

        # Wait for Textract to process the document
        result = None
        while True:
            status = TEXTRACT_CLIENT.get_document_text_detection(JobId=job_id)
            if status['JobStatus'] in ['SUCCEEDED', 'FAILED']:
                result = status
                break
        if status['JobStatus'] == 'FAILED':
            raise HTTPException(status_code=500, detail="Textract failed to analyze the document.")
        # Return the analysis result
        textract_result = open_textract_json(result)
        return {"job_status": status['JobStatus'], "result": textract_result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@api_router.post("/parseOcr/")
async def parse_ocr_answer(ocr_answer: List[str]):
    try:
        response = AWS_ANSWER_PARSER_AGENT.invoke_agent(
            agentId='REMJZIU22D',
            agentAliasId='G5ECOLYTGP',
            sessionId='session-6',
            inputText='\n'.join(ocr_answer)
        )

        event_stream = response['completion']

        for event in event_stream:

            if 'chunk' in event:
                chunk_data = event['chunk']['bytes'].decode('utf-8')
                response = json.loads(chunk_data)
                return response

    except Exception as e:
        print(f"Error al invocar el modelo: {str(e)}")
        return {"error": str(e)}



@api_router.post("/pauta/")
async def upload_file(file: UploadFile = File(...)):
    AWS_S3_CLIENT.upload_fileobj(
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
            AWS_S3_CLIENT.upload_fileobj(
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
@api_router.post("/prueba/")
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