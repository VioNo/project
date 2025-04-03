from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import declarative_base
from app.pages.config import POSTGRES_DATABASE_URL
from pydantic_settings import BaseSettings

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