import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
import app.pages.main_back as app

client = TestClient(app)

@pytest.mark.asyncio
async def test_register():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/register", data={
            "login_user": "testuser",
            "email": "testuser@example.com",
            "password": "password123",
            "password_confirm": "password123"
        })
        assert response.status_code == 201
        assert response.json()["detail"] == "User registered successfully"

@pytest.mark.asyncio
async def test_create_new_task():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        ac.cookies.set("access_token", "Bearer valid_token")
        response = await ac.post("/tasks/create", data={
            "user_id": 1,
            "title": "Test Task",
            "description": "This is a test task",
            "status": "pending"
        })
        assert response.status_code == 200
        assert response.json()["title"] == "Test Task"

@pytest.mark.asyncio
async def test_delete_existing_task():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        ac.cookies.set("access_token", "Bearer valid_token")
        response = await ac.delete("/tasks/1")
        assert response.status_code == 200
        assert response.json()["detail"] == "Task deleted"
