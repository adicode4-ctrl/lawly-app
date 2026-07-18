import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Force load the .env file from the backend folder
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
env_path = os.path.join(backend_dir, ".env")
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    PROJECT_NAME: str = "Lawly AI"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")

    class Config:
        extra = "ignore"

# Create the instance
settings = Settings()