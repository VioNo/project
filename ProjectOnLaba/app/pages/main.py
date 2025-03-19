
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Request, status, Form, Response
from sqlalchemy.ext.asyncio import AsyncSession
from watchfiles import awatch

from app.pages.database import get_session
from fastapi.responses import RedirectResponse
from app.pages.schemas import  TaskCreate
from app.pages.crud import create_user, create_task, get_tasks, update_task, delete_task, get_task, found_user
from app.pages.auth import get_payload, encode_jwt, decode_jwt
from contextlib import asynccontextmanager
from fastapi.templating import Jinja2Templates
from typing import Annotated



# Jinja2
router = APIRouter(prefix='', tags=['API'])

app = FastAPI()

templates = Jinja2Templates(directory='app/templates')

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

@router.get('/')
async def get_main_page(request: Request):
    return templates.TemplateResponse(name='index.html', context={'request': request})

@app.post("/register", status_code=status.HTTP_201_CREATED)
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


@app.post("/login")
async def login(
        response: Response,
        login_user: str = Form(...),
        password: str = Form(...),
        db: AsyncSession = Depends(get_session)
):
    user = await found_user(login_user, password, db)
    if user is None:
        raise HTTPException(status_code=401, detail="You're not registered")
    payload = {"user_id": user.id}
    token = encode_jwt(payload)
    response.set_cookie(key="users_access_token", value=token, httponly=True)
    #вывод токена
    payload_new = await get_payload(token)
    # return RedirectResponse(url=f"/tasks_of_user/{user.id}", status_code=status.HTTP_302_FOUND)
    return {
        "Токен id": payload_new["user_id"],
        "Токен истекает в": payload_new["exp"],
        "user_id из URL": user.id,
    }

@app.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}

@app.get("/tasks_of_user/{user_id}")
async def read_tasks(
        request: Request,
        user_id: int,
        token: str,
        db: AsyncSession = Depends(get_session)):

    token = await get_payload()
    return {
        "Токен id": token["user_id"],
        "Токен истекает в": token["exp"],
        "user_id из URL": user_id,
    }
    # try:
    #     payload = decode_jwt(token)
    # except:
    #     return {"error": "UNAUTHORIZED_ERROR"}
    # tasks = await get_user_tasks_id(db, user_id)
    # return templates.TemplateResponse("tasks.html", {"request": request, "tasks": tasks, "user_id": user_id})

@app.get("/tasks")
async def read_tasks(status: str = None, token = Depends(get_payload), db: AsyncSession = Depends(get_session)):
    tasks = await get_tasks(db, status)
    return tasks

@app.get("/tasks/{task_id}")
async def read_task(task_id: int, token = Depends(get_payload), db: AsyncSession = Depends(get_session)):
    db_task = await get_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.post("/tasks/create")
async def create_new_task(
    token = Depends(get_payload),
    user_id: int = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    status: str = Form(...),
    db: AsyncSession = Depends(get_session)
):
    task = TaskCreate(title=title, description=description, status=status)
    db_task = await create_task(db, task, user_id)
    return db_task

@app.put("/tasks/{task_id}")
async def update_existing_task(task_id: int,
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    status: Annotated[str, Form()],
    db: AsyncSession = Depends(get_session),
    token = Depends(get_payload)
):
    task = TaskCreate(title=title, description=description, status=status)
    db_task = await update_task(db, task_id, task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.delete("/tasks/{task_id}")
async def delete_existing_task(task_id: int, token = Depends(get_payload), db: AsyncSession = Depends(get_session)):
    db_task = await delete_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}

# @app.get("/tasks_of_user/{user_id}")
# async def read_tasks(request: Request, user_id: int, db: AsyncSession = Depends(get_session)):
#     tasks = await get_user_tasks_id(db, user_id)
#     return templates.TemplateResponse("tasks.html", {"request": request, "tasks": tasks, "user_id": user_id})
#
# @app.get("/tasks")
# async def read_tasks(status: str = None, db: AsyncSession = Depends(get_session)):
#     tasks = await get_tasks(db, status)
#     return tasks
#
# @app.get("/tasks/{task_id}")
# async def read_task(task_id: int, db: AsyncSession = Depends(get_session)):
#     db_task = await get_task(db, task_id)
#     if db_task is None:
#         raise HTTPException(status_code=404, detail="Task not found")
#     return db_task
#
# @app.post("/tasks/create")
# async def create_new_task(
#     user_id: int = Form(...),
#     title: str = Form(...),
#     description: str = Form(...),
#     status: str = Form(...),
#     db: AsyncSession = Depends(get_session)
# ):
#     task = TaskCreate(title=title, description=description, status=status)
#     db_task = await create_task(db, task, user_id)
#     return db_task
#
# @app.put("/tasks/{task_id}")
# async def update_existing_task(task_id: int, title: Annotated[str, Form()], description: Annotated[str, Form()], status: Annotated[str, Form()], db: AsyncSession = Depends(get_session)):
#     task = TaskCreate(title=title, description=description, status=status)
#     db_task = await update_task(db, task_id, task)
#     if db_task is None:
#         raise HTTPException(status_code=404, detail="Task not found")
#     return db_task
#
# @app.delete("/tasks/{task_id}")
# async def delete_existing_task(task_id: int, db: AsyncSession = Depends(get_session)):
#     db_task = await delete_task(db, task_id)
#     if db_task is None:
#         raise HTTPException(status_code=404, detail="Task not found")
#     return {"detail": "Task deleted"}

app.include_router(router)
