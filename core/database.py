import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environment variables from .env file (optional)
load_dotenv()

# SQLAlchemy Base
Base = declarative_base()

# Environment-specific configurations
ENV = os.getenv("ENV", "development")  # Default to development if ENV is not set 



if ENV == "development":
    # Local PostgreSQL settings
    DB_USER = os.getenv("DEV_DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DEV_DB_PASSWORD", "password")
    DB_HOST = os.getenv("DEV_DB_HOST", "192.168.1.167")
    DB_PORT = os.getenv("DEV_DB_PORT", "5432")
    DB_NAME = os.getenv("DEV_DB_NAME", "dev_db")

elif ENV == "production":
    # AWS PostgreSQL settings
    DB_USER = os.getenv("PROD_DB_USER")
    DB_PASSWORD = os.getenv("PROD_DB_PASSWORD")
    DB_HOST = os.getenv("PROD_DB_HOST")
    DB_PORT = os.getenv("PROD_DB_PORT")
    DB_NAME = os.getenv("PROD_DB_NAME")

else:
    raise ValueError("Invalid ENV value. Use 'development' or 'production'.")

# Construct the database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy engine and session
engine = create_engine(DATABASE_URL, pool_pre_ping=True)  # Pre-ping ensures live connection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for FastAPI to use DB sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
