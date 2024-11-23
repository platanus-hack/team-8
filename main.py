# FastAPI Imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Libraries Imports
from dotenv import load_dotenv
from typing import List

# Local Imports
from api.v1.routes import api_router

load_dotenv()


app = FastAPI(
    title="My FastAPI Project",
    version="1.0.0"
)

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


app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": f'Home Page'}