from fastapi import APIRouter, HTTPException, Depends, Response, Form, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session
from backend.db.database import get_db
from backend.models.models import User
from backend.db.refresh_token import store_refresh_token
from backend.core.settings import settings
from backend.core.cryptography import encrypt, decrypt
from backend.account.auth import signup
from pwdlib import PasswordHash
from uuid import uuid4
from backend.core.hashing import hash_token, verify_token
from backend.core.auth_handler import (
    create_access_token,
    create_refresh_token,
    refresh_access_token,
    decode_jwt,
)
from datetime import datetime, timedelta, timezone

hasher = PasswordHash.recommended()

router = APIRouter()


@router.post("/sign-up", status_code=201)
def signup_endpoint(
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    client_key: str = Form(...),
    client_secret: str = Form(...),
    db: Session = Depends(get_db),
):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hasher.hash(password)
    encrypted_api_key = encrypt(client_key)
    encrypted_api_secret = encrypt(client_secret)
    existing = (
        db.query(User).filter(User.encrypted_api_key == encrypted_api_key).first()
        or db.query(User)
        .filter(User.encrypted_secret_key == encrypted_api_secret)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="API Key/Secret already in use")
    else:
        new_user = signup(
            db,
            email,
            hashed_password,
            encrypted_api_key,
            encrypted_api_secret,
        )
        access_token = create_access_token(str(new_user.id))
        jti = str(uuid4())
        refresh_token = create_refresh_token(str(new_user.id), jti)
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
        )

        return RedirectResponse(url="/profile", status_code=303)


@router.post("/login", status_code=201)
def login_endpoint(
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
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
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="strict",
        )
        store_refresh_token(
            db,
            refresh_token,
            existing.id,
            jti,
            datetime.now(timezone.utc)
            + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )
        return {"access_token": access_token, "token_type": "Bearer"}

    else:
        raise HTTPException(status_code=401, detail="Invalid password")


@router.post("/refresh-access-token")
def refresh_access_token_endpoint(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401)
    new_access = refresh_access_token(refresh_token)
    if not new_access:
        raise HTTPException(status_code=401)
    return {"access_token": new_access}


def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401)
    access_token = decode_jwt(token)
    user_id = access_token.get("sub")
    if not user_id:
        raise HTTPException(status_code=401)
    return user_id
