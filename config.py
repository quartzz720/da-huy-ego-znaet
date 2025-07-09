import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_ID: int
    DATABASE_URL: str = 'sqlite:///./db.sqlite3'
    WEBAPP_URL: str = 'http://localhost:8000'

    class Config:
        env_file = '.env'

settings = Settings()
