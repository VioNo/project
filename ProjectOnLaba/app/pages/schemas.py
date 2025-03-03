from enum import Enum
from datetime import datetime, date
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# перечисление для task
class Status(str, Enum):
    pending = "Pending"
    new = "New"
    progr = "In Progress"
    comp = "Completed"


# все что связано с user
class UserBase(BaseModel):
    login: str
    email: EmailStr

class UserCreate(UserBase):
    password_hash: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True



# все что связано с task
date_only = datetime.now().date()

class TaskBase(BaseModel):
    title: Optional[str] = "Task"
    description: Optional[str] = "Description for Task"
    status: Status = Field(default=...)
    create_at: Optional[date] = date_only

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
