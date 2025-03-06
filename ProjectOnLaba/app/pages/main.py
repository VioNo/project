from fastapi import FastAPI, Depends, HTTPException, APIRouter, Request, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.pages.database import get_session
from app.pages.schemas import UserCreate, TaskCreate
from app.pages.crud import create_user, create_task, get_tasks, update_task, delete_task, get_task, get_user_tasks, get_user_by_email, found_user
from app.pages.auth import authenticate_user, create_access_token, get_password_hash
from contextlib import asynccontextmanager
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm

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
async def register(user: UserCreate, db: AsyncSession = Depends(get_session)):
    if user.password != user.password_confirm:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    db_user = await create_user(db, user)
    return {"detail": "User registered successfully", "user": db_user}

# @app.post("/register", status_code=status.HTTP_201_CREATED)
# async def register(user: UserCreate, db: AsyncSession = Depends(get_session)):
#     if user.password != user.password_confirm:
#         raise HTTPException(status_code=400, detail="Passwords do not match")
#     db_user = await create_user(db, user)
#     return {"User registered successfully", "user", db_user}

@app.post("/login")
async def login(login: str = Form(...), password: str = Form(...), db: AsyncSession = Depends(get_session)):
    user = await found_user(login, password, db)
    if user is None:
        raise HTTPException(status_code=401, detail="you're not registered")
    return {"detail": "You have successfully logged in"}


# @app.post("/login")
# async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
#     user = await authenticate_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token = create_access_token(data={"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}

@app.get("/tasks_of_user/{login}")
async def read_tasks(login: str, db: AsyncSession = Depends(get_session)):
    tasks = await get_user_tasks(db, login)
    return tasks

@router.get('/tasks')
async def read_tasks_html(request: Request, tasks=Depends(read_tasks)):
    return templates.TemplateResponse(name='task.html', context={'request': request, 'tasks': tasks})

@app.get("/tasks")
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
    return templates.TemplateResponse(
        "task_up.html",
        {"task_up": db_task}
    )

@app.delete("/tasks/{task_id}")
async def delete_existing_task(task_id: int, db: AsyncSession = Depends(get_session)):
    db_task = await delete_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}

app.include_router(router)
