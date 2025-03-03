from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.pages.models import User, Task
from app.pages.schemas import UserCreate, TaskCreate
from passlib.context import CryptContext
from random import randint
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalar_one_or_none()

#create_user
async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(id = randint(100, 10000) ,login=user.login, email=user.email, password_hash=user.hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
#create_task
async def create_task(db: AsyncSession, task: TaskCreate, user_id: int):
    db_task = Task(**task.dict(), user_id=user_id)
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task
#get_user_tasks
async def get_user_tasks(db: AsyncSession, user_id: int):
    query = select(Task)
    if user_id:
        query = query.filter(Task.user_id == user_id)
    result = await db.execute(query)
    return result.scalars().all()
#get_tasks
async def get_tasks(db: AsyncSession, status: str = None):
    query = select(Task)
    if status:
        query = query.filter(Task.status == status)
    result = await db.execute(query)
    return result.scalars().all()
#get_task
async def get_task(db: AsyncSession, task_id: int):
    result = await db.execute(select(Task).filter(Task.id == task_id))
    return result.scalar_one_or_none()
#update_task
async def update_task(db: AsyncSession, task_id: int, task: TaskCreate):
    db_task = await get_task(db, task_id)
    if db_task:
        db_task.title = task.title
        db_task.description = task.description
        db_task.status = task.status
        await db.commit()
        await db.refresh(db_task)
    return db_task
#delete_task
async def delete_task(db: AsyncSession, task_id: int):
    db_task = await get_task(db, task_id)
    if db_task:
        await db.delete(db_task)
        await db.commit()
    return db_task
