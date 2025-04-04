from fastapi import APIRouter, Form, FastAPI, Request, Response, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_session
from .crud import found_user
from .auth import encode_jwt
from contextlib import asynccontextmanager
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix='', tags=['API_front'])
app = FastAPI()
templates = Jinja2Templates(directory='templates')

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

@router.get('/')
async def get_main_page(request: Request):
    return templates.TemplateResponse(name='index.html', context={'request': request})

@router.post("/login")
async def login(
        response: Response,
        login_user: str = Form(...),
        password: str = Form(...),
        db: AsyncSession = Depends(get_session)
):
    user = await found_user(login_user, password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    payload = {"user_id": user.id}
    token = encode_jwt(payload)  # Ваша функция генерации JWT
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",  # Добавляем префикс Bearer
        httponly=True,
        max_age=1800,
        secure=False,  # True в production
        samesite="lax",
        path="/"
    )
    return {"user_id": user.id}

@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(key="access_token")
    return {'message': 'Пользователь успешно вышел из системы'}

app.include_router(router)