from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from boto3 import client
import os
from dotenv import load_dotenv

load_dotenv()


AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_ACCESS_KEY_VALUE = os.getenv('AWS_ACCESS_KEY_VALUE')
S3_BUCKET = 'meayudai-files'


AWS_CLIENT = client(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_ACCESS_KEY_VALUE, service_name='s3')


TEXTRACT_CLIENT = client(
    'textract',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_ACCESS_KEY_VALUE,
    region_name='us-west-2'  # Cambia por la región correcta
)


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
    #AWS_CLIENT.upload_file(f'data/prueba lourdes completa.pdf', S3_BUCKET, f'test/test5.pdf')
    return {"message": f'buckets: {buckets}'}


@app.get("/list_files/")
async def list_files():
    """
    List all files in the S3 bucket.
    
    Returns:
    - List of files in the S3 bucket.
    """
    try:
        # List all files in the S3 bucket
        files = AWS_CLIENT.list_objects(Bucket=S3_BUCKET)
        files_list = [file['Key'] for file in files['Contents']]
        
        # Return the list of files
        return files_list
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/analyze/")
async def analyze_file_s3(file_key: str):
    """
    Send a file from S3 to AWS Textract and return the response.
    
    Parameters:
    - file_key (str): The key of the file in the S3 bucket.

    Returns:
    - Textract analysis result.
    """
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
        return {"job_status": status['JobStatus'], "result": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")