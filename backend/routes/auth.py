from fastapi import APIRouter, HTTPException, Depends, Response
from sqlmodel import Session
from db.database import get_db
from models.models import User
from db.refresh_token import store_refresh_token
from core.settings import settings
from core.cryptography import encrypt, decrypt
from account.auth import signup
from pwdlib import PasswordHash
from uuid import uuid4
from core.hashing import hash_token, verify_token
from core.auth_handler import create_access_token, create_refresh_token, refresh_token
from datetime import datetime, timedelta

hasher = PasswordHash.recommended()

router = APIRouter()


@router.post("/sign-up", status_code=201)
def signup_endpoint(
    email: str,
    password: str,
    api_key: str,
    secret_key: str,
    db: Session = Depends(get_db),
):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hasher.hash(password)
    encrypted_api_key = encrypt(api_key)
    encrypted_api_secret = encrypt(secret_key)

    new_user = signup(
        db, email, hashed_password, encrypted_api_key, encrypted_api_secret
    )
    return {"id": new_user.id, "email": new_user.email}


@router.post("/login", status_code=201)
def login_endpoint(
    response: Response,
    email: str,
    password: str,
    db: Session = Depends(get_db),
):
    existing = db.query(User).filter(User.email == email).first()
    if not existing:
        raise HTTPException(status_code=400, detail="User not found")
    verify_password = hasher.verify(password, existing.hashed_password)
    if verify_password:
        access_token = create_access_token(str(existing.id))
        jti = str(uuid4())
        refresh_token = create_refresh_token(str(existing.id), jti)
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
        )
        store_refresh_token(
            db,
            refresh_token,
            existing.id,
            jti,
            datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )
        return {"access_token": access_token}

    else:
        raise HTTPException(status_code=401, detail="Invalid password")


@router.post("/refresh")
def refresh_token(refresh_token: str):
    new_token = refresh_token()
