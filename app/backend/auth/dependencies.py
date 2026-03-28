from sqlmodel import Session, select, or_
from fastapi import Response, HTTPException, Depends, Request
from backend.models.models import User, RefreshToken
from backend.auth.schema import SignupData, LoginRequest
from backend.auth.db import create_user, hash_and_store_refresh_token
from backend.auth.tokens import (
    generate_tokens,
    create_access_token,
    create_refresh_token,
    decode_jwt,
)
from backend.core.cryptography import encrypt
from pwdlib import PasswordHash
from uuid import uuid4
from datetime import datetime, timezone, timedelta
from backend.core.settings import settings
from backend.db.database import get_db
from backend.services.tradingClient import get_alpaca_client

hasher = PasswordHash.recommended()


def create_user_and_tokens(db: Session, data: SignupData):
    # Checks if email already in use
    statement = select(User).where(User.email == data.email)
    existing = db.exec(statement).first()
    if existing:
        raise ValueError("User already exists")

    # Checks if api key/secret already in use
    encrypted_api_key = encrypt(data.client_key)
    encrypted_api_secret = encrypt(data.client_secret)
    statement = select(User).where(
        or_(
            User.encrypted_api_key == encrypted_api_key,
            User.encrypted_secret_key == encrypted_api_secret,
        )
    )
    existing = db.exec(statement).first()
    if existing:
        raise ValueError("API Key/Secret already in use")

    # Creates user in database
    hashed_password = hasher.hash(data.password)
    new_user = create_user(
        db,
        data.first_name,
        data.last_name,
        data.email,
        hashed_password,
        encrypted_api_key,
        encrypted_api_secret,
    )

    # Creates access and refresh token for user
    access_token, refresh_token, jti = generate_tokens(new_user)
    expires_at = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    hash_and_store_refresh_token(db, refresh_token, new_user.id, jti, expires_at)
    return new_user, access_token, refresh_token


def validate_user(login: LoginRequest, db: Session = Depends(get_db)) -> User:
    statement = select(User).where(User.email == login.email)
    user = db.exec(statement).first()

    if not user or not hasher.verify(login.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    return user


def refresh_tokens(
    refresh_token_str: str,
    db: Session,
    response: Response,
) -> str:
    # Decodes payload
    payload = decode_jwt(refresh_token_str)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    jti = payload.get("jti")
    if not jti:
        raise HTTPException(status_code=401, detail="Malformed refresh token")

    # Look up in db
    statement = select(RefreshToken).where(RefreshToken.jti == jti)
    token_record = db.exec(statement).first()
    if not token_record or token_record.revoked:
        raise HTTPException(status_code=401, detail="Refresh token revoked")

    # Check expiration
    if token_record.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Refresh token expired")

    # Create new access token
    user_id = payload["sub"]
    new_access = create_access_token(user_id)

    # Refresh rotation
    new_jti = str(uuid4())
    new_refresh = create_refresh_token(user_id, new_jti)
    token_record.revoked = True
    db.add(token_record)
    db.commit()

    statement = select(User).where(User.id == user_id)
    expires_at = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    hash_and_store_refresh_token(db, new_refresh, user_id, new_jti, expires_at)

    # Set fresh refresh cookie
    response.set_cookie(
        "refresh_token",
        new_refresh,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
        path="/",
    )

    return new_access


def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401)

    user_id = decode_jwt(token).get("sub")
    if not user_id:
        raise HTTPException(status_code=401)
    user = db.query(User).get(user_id)
    return user
