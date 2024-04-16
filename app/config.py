from pydantic_settings import BaseSettings
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Settings(BaseSettings):
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str

    class Config:
        env_file = ".env"


settings = Settings()