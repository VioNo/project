from fastapi import FastAPI, Depends, HTTPException, APIRouter, Request, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_session
from fastapi.responses import RedirectResponse
from .schemas import  TaskCreate
from .crud import create_user, create_task, get_tasks, update_task, delete_task, get_task, get_user_tasks_id
from .auth import decode_jwt
from contextlib import asynccontextmanager
from fastapi.templating import Jinja2Templates
from typing import Annotated
from fastapi.security import HTTPBearer

# Jinja2
router = APIRouter(prefix='', tags=['API_back'])
security = HTTPBearer()
app = FastAPI()
templates = Jinja2Templates(directory='templates')

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    login_user: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    password_confirm: str = Form(...),
    db: AsyncSession = Depends(get_session)
):
    if password != password_confirm:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    db_user = await create_user(db, login_user, email, password)
    return {"detail": "User registered successfully", "user": db_user}

@router.get("/tasks_of_user/{user_id}")
async def read_tasks(
        request: Request,
        user_id: int,
        db: AsyncSession = Depends(get_session)
):
    try:
        # Получаем токен из куки
        token = request.cookies.get("access_token")
        # Удаляем 'Bearer ' если есть
        if token.startswith("Bearer "):
            token = token[7:]
        payload = decode_jwt(token)
        # Проверяем соответствие user_id
        if int(payload["user_id"]) != int(user_id):
            return RedirectResponse(url="/")

        tasks = await get_user_tasks_id(db, user_id)
        return templates.TemplateResponse(
            "tasks.html",
            {"request": request, "tasks": tasks, "user_id": user_id}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error processing request: {str(e)}"
        )

@router.get("/tasks")
async def read_tasks(request: Request, status: str = None, db: AsyncSession = Depends(get_session)):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/")
    else:
        tasks = await get_tasks(db, status)
    return tasks


@router.get("/tasks/{task_id}")
async def read_task(request: Request, task_id: int, db: AsyncSession = Depends(get_session)):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/")
    else:
        db_task = await get_task(db, task_id)
        if db_task is None:
            raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.post("/tasks/create")
async def create_new_task(
    request: Request,
    user_id: int = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    status: str = Form(...),
    db: AsyncSession = Depends(get_session)
):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/")
    if token.startswith("Bearer "):
        token = token[7:]
    try:
        payload = decode_jwt(token)
        if int(payload["user_id"]) != int(user_id):
            return RedirectResponse(url="/")
        task = TaskCreate(title=title, description=description, status=status)
        db_task = await create_task(db, task, user_id)
        return db_task
    except Exception as e:
        return RedirectResponse(url="/")

@router.put("/tasks/{task_id}")
async def update_existing_task(
        request: Request,
        task_id: int,
        title: Annotated[str, Form()],
        description: Annotated[str, Form()],
        status: Annotated[str, Form()],
        db: AsyncSession = Depends(get_session),
    ):

    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/")

    task = TaskCreate(title=title, description=description, status=status)
    db_task = await update_task(db, task_id, task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.delete("/tasks/{task_id}")
async def delete_existing_task(request: Request, task_id: int, db: AsyncSession = Depends(get_session)):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/")

    db_task = await delete_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}

app.include_router(router)
