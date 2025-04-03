from fastapi import FastAPI, Depends, HTTPException, APIRouter, Request, status, Form, Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from fastapi.templating import Jinja2Templates
from typing import Annotated, Optional
from jose import jwt
from datetime import datetime, timedelta, timezone, date
import uvicorn
from sqlalchemy.future import select
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from enum import Enum
from pydantic import BaseModel, Field, EmailStr