from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()
POSTGRES_DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(POSTGRES_DATABASE_URL, echo=True)

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str

settings = Settings()


def get_auth_data():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}


Base = declarative_base()

async def get_session():
    async with AsyncSession(engine) as session:
        yield session


