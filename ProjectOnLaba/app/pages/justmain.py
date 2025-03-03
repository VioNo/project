from fastapi import FastAPI
from app.dao.router import router as router_task


app = FastAPI()


@app.get("/")
def home_page():
    return {"message": "Привет, Хабр!"}


app.include_router(router_task)