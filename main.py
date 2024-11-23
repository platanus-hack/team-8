from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from boto3 import client
import os
from dotenv import load_dotenv

load_dotenv()


AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_ACCESS_KEY_VALUE = os.getenv('AWS_ACCESS_KEY_VALUE')
S3_BUCKET = 'meayudai-files'
# Directory to save uploaded files
UPLOAD_DIR = "uploads"

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
    # Save file
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())
    
    return {"filename": file.filename, "message": "File uploaded successfully!"}

@app.post("/prueba/")
async def upload_file(file: UploadFile = File(...)):
    # Save file
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())
    
    return {"filename": file.filename, "message": "File uploaded successfully!"}