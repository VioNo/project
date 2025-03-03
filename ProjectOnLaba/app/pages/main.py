from fastapi import FastAPI, Depends, HTTPException, APIRouter, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.pages.database import get_session
from app.pages.schemas import UserCreate, TaskCreate
from app.pages.crud import create_user, create_task, get_tasks, update_task, delete_task, get_task, get_user_tasks
from app.pages.auth import authenticate_user, create_access_token
from contextlib import asynccontextmanager
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Jinja2
router = APIRouter(prefix='', tags=['API'])

app = FastAPI() #экземпляр приложения FastAPI, используется для определения маршрутов (эндпоинтов) и управления жизненным циклом приложения.


templates = Jinja2Templates(directory='app/templates')

@asynccontextmanager #определяет асинхронный контекстный менеджер
async def lifespan(app: FastAPI):
    yield

@router.get('/')
async def get_main_page(request: Request):
    return templates.TemplateResponse(name='index.html', context={'request': request})


@app.post("/register") #декоратор, определяющ маршрут (эндпоинт) для обработки HTTP POST-запросов по адресу /register
async def register( user: UserCreate, db: AsyncSession = Depends(get_session)):
    db_user = await create_user(db, user)
    return db_user

@app.post("/login")
async def login(user: UserCreate, db: AsyncSession = Depends(get_session)):
    user = await authenticate_user(db, user.email, user.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/tasks_of_user/{user_id}")
async def read_tasks(user_id: int, db: AsyncSession = Depends(get_session)):
    tasks = await get_user_tasks(db, user_id)
    return tasks


@router.get('/tasks')
async def read_tasks_html(request: Request, tasks=Depends(read_tasks)):
    return templates.TemplateResponse(name='task.html', context={'request': request, 'tasks': tasks })
# @app.get("/tasks")
async def read_tasks(status: str = None, db: AsyncSession = Depends(get_session)):
    tasks = await get_tasks(db, status)
    return tasks

@app.get("/tasks/{task_id}")
async def read_task(task_id: int, db: AsyncSession = Depends(get_session)):
    db_task = await get_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.post("/tasks/create")
async def create_new_task(user_id: int, task: TaskCreate, db: AsyncSession = Depends(get_session)):
    db_task = await create_task(db, task, user_id)
    return db_task


@app.put("/tasks/{task_id}")
async def update_existing_task(task_id: int, task: TaskCreate, db: AsyncSession = Depends(get_session)):
    db_task = await update_task(db, task_id, task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    # Возвращаем HTML-ответ с использованием шаблона
    return templates.TemplateResponse(
        "task_up.html",
        {"request": Request, "task_up": db_task}
    )

# @app.put("/tasks/{task_id}")
# async def update_existing_task(task_id: int, task: TaskCreate, db: AsyncSession = Depends(get_session)):
#     db_task = await update_task(db, task_id, task)
#     if db_task is None:
#         raise HTTPException(status_code=404, detail="Task not found")
#     return db_task

@app.delete("/tasks/{task_id}")
async def delete_existing_task(task_id: int, db: AsyncSession = Depends(get_session)):
    db_task = await delete_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}

app.include_router(router)