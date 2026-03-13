from fastapi import APIRouter, Depends, Request, Response, HTTPException
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from backend.models.models import User
from .auth import get_current_user
from backend.db.database import get_db
from backend.core.auth_handler import (
    decode_jwt,
)

router = APIRouter()

templates = Jinja2Templates(directory="frontend/templates")


# @router.get("/me")
# def get_me(user_id: str = Depends(get_current_user)):
#     return {"user_id": user_id}


@router.get("/profile")
def profile(request: Request, user: User = Depends(get_current_user)):
    formatted_date = user.created_at.strftime("%d-%m-%Y")
    return templates.TemplateResponse(
        "profile.html",
        {"request": request, "user": user, "created_at_str": formatted_date},
    )
