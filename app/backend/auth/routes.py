from typing import Annotated
from fastapi import APIRouter, Response, Request, Depends, HTTPException, Form
from fastapi.responses import RedirectResponse
from sqlmodel import Session
from backend.db.database import get_db
from backend.models.models import User
from backend.auth.schema import SignupData, LoginRequest
from backend.auth.dependencies import (
    create_user_and_tokens,
    refresh_tokens,
    validate_user,
)
from backend.auth.tokens import generate_tokens
from backend.core.settings import settings
from datetime import datetime, timezone, timedelta
from backend.auth.db import hash_and_store_refresh_token

router = APIRouter(tags=["auth"])


@router.post("/sign-up", status_code=201)
def signup_endpoint(
    response: Response,
    data: Annotated[SignupData, Form()],
    db: Session = Depends(get_db),
):
    try:
        user, access_token, refresh_token = create_user_and_tokens(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    response = RedirectResponse(url="/client/profile", status_code=303)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=settings.JWT_EXPIRATION_MINUTES * 60,
        path="/",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
        path="/",
    )

    return response


@router.post("/log-in", status_code=201)
def login_endpoint(
    response: Response,
    data: Annotated[LoginRequest, Form()],
    db: Session = Depends(get_db),
):
    # Manually validate
    user = validate_user(data, db)

    access_token, refresh_token, jti = generate_tokens(user)

    expires_at = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    hash_and_store_refresh_token(db, refresh_token, user.id, jti, expires_at)

    response = RedirectResponse(url="/client/profile", status_code=303)
    response.set_cookie(
        "access_token",
        access_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=settings.JWT_EXPIRATION_MINUTES * 60,
        path="/",
    )
    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
        path="/",
    )

    return response


@router.post("/refresh")
def refresh_endpoint(
    request: Request, response: Response, db: Session = Depends(get_db)
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token mission")

    new_access = refresh_tokens(refresh_token, db, response)

    response.set_cookie(
        "access_token",
        new_access,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=settings.JWT_EXPIRATION_MINUTES * 60,
        path="/",
    )

    return {"access_token": "refreshed"}


@router.post("/logout", status_code=202)
def logout_endpoint(response: Response):

    # Redirect to home page
    response = RedirectResponse("/home", status_code=303)

    # Clear cookies
    response.delete_cookie(key="access_token", path="/")
    response.delete_cookie(key="refresh_token", path="/")

    return response
