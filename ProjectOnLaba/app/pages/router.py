from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix='/app', tags=['Фронтенд'])
templates = Jinja2Templates(directory='app/main')


@router.get('/task_html')
async def get_task_html(request: Request):
    return templates.TemplateResponse(name='task.html', context={'request': request})