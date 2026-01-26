from fastapi import APIRouter, HTTPException
from sqlmodel import Session
from db.database import get_db
from models.models import User
from core.settings import settings

router = APIRouter()
