from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from db.database import get_db
from models.models import TestUser
from core.settings import settings
from account.auth import signup

router = APIRouter()


@router.post("/sign-up", status_code=201)
def signup_endpoint(
    email: str,
    password: str,
    api_key: str,
    secret_key: str,
    db: Session = Depends(get_db),
):
    existing = db.query(TestUser).filter(TestUser.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = signup(db, email, password, api_key, secret_key)
    return {"id": new_user.id, "email": new_user.email}
