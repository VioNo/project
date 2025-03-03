from fastapi import APIRouter
from sqlalchemy import select
from app.pages.database import get_session
from app.pages.models import Task

router = APIRouter(prefix='/Task', tags=['Работа с Tasks'])

@router.get("/", summary="Получить все Tasks")
async def read_tasks():
    async with get_session() as session:
        query = select(Task)
        result = await session.execute(query)
        task = result.scalars().all()
        return task