from contextlib import asynccontextmanager
from fastapi import FastAPI
from .main_back import router as router_back
from .main_front import router as router_front

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router_back)
app.include_router(router_front)

