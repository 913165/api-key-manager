# app/core/config.py
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "API Key Manager"
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()