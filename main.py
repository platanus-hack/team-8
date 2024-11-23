# FastAPI Imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from supabase import create_client, Client
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Libraries Imports
from dotenv import load_dotenv
from typing import List

# Local Imports
from api.v1.routes import api_router

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def get_supabase_client() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Faltan las variables de configuración de Supabase")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


supabase_client = get_supabase_client()


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


class User(BaseModel):
    email: str

@app.post("/users")
async def add_user(user: User):
    """Guarda un nuevo usuario en Supabase"""
    # Inserta el usuario en la tabla "users"
    response = supabase_client.table("users").insert(user.dict()).execute()
    
    return {"message": "Usuario guardado exitosamente", "data": response.data}