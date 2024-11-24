# FastApi Imports
from fastapi import APIRouter, File, UploadFile, HTTPException

# Libraries Imports
import threading
import queue
import os
from boto3 import client
from typing import List, Dict
import json
from supabase import create_client, Client

# Local Imports
from .services import open_textract_json
from db.schemas.test import Test
from db.schemas.student import Student
from db.schemas.student_answer import StudentAnswer
from db.schemas.guideline import Guideline
#from core.database import Base, engine

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_ACCESS_KEY_VALUE = os.getenv('AWS_ACCESS_KEY_VALUE')
S3_BUCKET = 'meayudai-files'
S3_REGION = 'oregon'
AWS_S3_CLIENT = client(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_ACCESS_KEY_VALUE, service_name='s3')
AWS_ANSWER_PARSER_AGENT = client(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_ACCESS_KEY_VALUE, service_name='bedrock-agent-runtime', region_name='us-west-2')
UPLOAD_DIR = "data"
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def get_supabase_client() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Faltan las variables de configuración de Supabase")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


supabase_client = get_supabase_client()


os.makedirs(UPLOAD_DIR, exist_ok=True)


TEXTRACT_CLIENT = client(
    'textract',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_ACCESS_KEY_VALUE,
    region_name='us-west-2'  # Cambia por la región correcta
)

AWS_BEDROCK_CLIENT = client(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_ACCESS_KEY_VALUE, service_name='bedrock-runtime', region_name='us-west-2')

def get_correct_exam_system_prompt(guideline, answer):
    system_prompt = (
        "You are an assistant for grading exams. "
        "You need to evaluate how accurate the student's answer is based on a guideline and the answer provided as context. "
        "The guideline has a structure of a dictionary where the main key is the question number, followed by a dictionary with each question and an outline of what is expected as the student's answer. "
        "The answer is a dictionary with the same structure, but it contains the student's responses. "
        "You must evaluate the accuracy of the student's answer on a scale from 1 to 10. "
        "Provide the result only as a dictionary in the following format: "
        "Question: { score: assigned_score, feedback: a brief comment explaining the assigned score }. "
        "Example output: "
        "{\"1\": { \"score\": 10, \"feedback\": \"The student's answer is correct as it includes all the key points of the expected answer.\" }, "
        "\"2\": { \"score\": 5, \"feedback\": \"The student's answer is incomplete as it misses a valid argument.\" }, ... }"
        "The guideline and the student's answer to evaluate are as follows: "
        f"Guideline: {guideline}. "
        f"Answer: {answer}. "
        "Please ensure that the output is in Spanish."
    )
    return system_prompt


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

@api_router.post("/correctExam/")
async def correct_exam(guideline: Dict, answer: Dict):
    try:
        response = AWS_BEDROCK_CLIENT.converse(
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            messages=[
                {
                    "role": "user",
                    "content": [{"text": "Corrige la prueba en base a la pauta y respuesta de tu system prompt"}]
                }
            ],
            system=[{"text": get_correct_exam_system_prompt(guideline, answer)}],
            inferenceConfig={
                "temperature": 0.8  # Optional: Set a max token limit
            }
        )
        if 'output' in response and 'message' in response['output']:
            content = response['output']['message']['content'][0]['text']
            print("Extracted Content:", content)
            try:
                parsed_content = json.loads(content)
                print("Parsed Content:", json.dumps(parsed_content, indent=2))
                return parsed_content
            except json.JSONDecodeError:
                print("Content is not JSON, returning as string")
                return {"result": content}
        return {"error": "No content in response"}

    except Exception as e:
        return {
            "error": str(e),
            "error_type": type(e).__name__
        }

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

# Model Enpoints

# CRUD for Tests
@api_router.post("/tests")
async def add_test(test: Test):
    """Create a new test in Supabase"""
    response = supabase_client.table("tests").insert(test.model_dump()).execute()

    return {"message": "Prueba guardada exitosamente", "data": response.data}
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"message": "Test created successfully", "data": response.data}

@api_router.get("/tests/{test_id}")
async def get_test(test_id: int):
    """Get a specific test by ID"""
    response = supabase_client.table("tests").select("*").eq("id", test_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Test not found")
    return {"data": response.data[0]}

@api_router.put("/tests/{test_id}")
async def update_test(test_id: int, test: Test):
    """Update a test by ID"""
    response = supabase_client.table("tests").update(test.model_dump()).eq("id", test_id).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"message": "Test updated successfully", "data": response.data}

@api_router.delete("/tests/{test_id}")
async def delete_test(test_id: int):
    """Delete a test by ID"""
    response = supabase_client.table("tests").delete().eq("id", test_id).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"message": "Test deleted successfully"}

# CRUD for Students
@api_router.post("/students")
async def add_student(student: Student):
    """Create a new student in Supabase"""
    response = supabase_client.table("students").insert(student.model_dump()).execute()
    return {"message": "Estudiante guardado exitosamente", "data": response.data}

@api_router.get("/students/{student_id}")
async def get_student(student_id: int):
    """Get a specific student by ID"""
    response = supabase_client.table("students").select("*").eq("id", student_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"data": response.data[0]}

@api_router.put("/students/{student_id}")
async def update_student(student_id: int, student: Student):
    """Update a student by ID"""
    response = supabase_client.table("students").update(student.model_dump()).eq("id", student_id).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"message": "Student updated successfully", "data": response.data}

@api_router.delete("/students/{student_id}")
async def delete_student(student_id: int):
    """Delete a student by ID"""
    response = supabase_client.table("students").delete().eq("id", student_id).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"message": "Student deleted successfully"}

# CRUD for Students' Answers
@api_router.post("/students_answers")
async def add_student_answer(student_answer: StudentAnswer):
    """Create a new student answer in Supabase"""
    response = supabase_client.table("students_answers").insert(student_answer.model_dump()).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"message": "Student answer created successfully", "data": response.data}

@api_router.get("/students_answers/{answer_id}")
async def get_student_answer(answer_id: int):
    """Get a specific student answer by ID"""
    response = supabase_client.table("students_answers").select("*").eq("id", answer_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Student answer not found")
    return {"data": response.data[0]}

@api_router.put("/students_answers/{answer_id}")
async def update_student_answer(answer_id: int, student_answer: StudentAnswer):
    """Update a student answer by ID"""
    response = supabase_client.table("students_answers").update(student_answer.model_dump()).eq("id", answer_id).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"message": "Student answer updated successfully", "data": response.data}

@api_router.delete("/students_answers/{answer_id}")
async def delete_student_answer(answer_id: int):
    """Delete a student answer by ID"""
    response = supabase_client.table("students_answers").delete().eq("id", answer_id).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"message": "Student answer deleted successfully"}

@api_router.get("/questions")
async def get_test_questions(test_id: int):
    """Get all test questions for a specific test"""
    response = supabase_client.table("questions").select("*").eq("test_id", test_id).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"message": "Test questions retrieved successfully"}

@api_router.get("/guidelines/")
async def get_guidelines():
    """Get all guidelines"""
    response = supabase_client.table("guidelines").select("*").execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"data": response.data}

@api_router.post("/guideline/")
async def add_guideline(guideline: Guideline):
    """Create a new guideline in Supabase"""
    response = supabase_client.table("guidelines").insert(guideline.model_dump()).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"message": "Guideline created successfully", "data": response.data}
