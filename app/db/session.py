# app/db/session.py
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database URL - replace with your actual database URL
#ATABASE_URL = "postgresql://user:password@localhost:5432/api_key_manager"
# get this url from .env file
DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        print(f"Database connection established: {db.bind.url}")

        yield db
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        raise
    finally:
        logger.info("Database connection closed")
        db.close()