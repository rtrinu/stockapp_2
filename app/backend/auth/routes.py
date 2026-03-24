from fastapi import APIRouter, Response, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from backend.db.database import get_db
from backend.models.models import User
from sqlmodel import select
from auth.schema import SignupData
from auth.dependencies import create_user_and_tokens, refresh_tokens
from auth.tokens import generate_tokens
from sqlmodel import Session
from core.settings import settings


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/sign-up", status_code=201)
def signup_endpoint(
    response: Response, data: SignupData, db: Session = Depends(get_db)
):
    # Calls function to create user and tokens
    try:
        user, access_token, refresh_token = create_user_and_tokens(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Redirects user to profile
    response = RedirectResponse(url="/clinet/profile", status_code=303)

    # Sets tokens in cookies
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
    user: User = Depends(validate_user),
    tokens: tuple = Depends(generate_tokens),
    db: Session = Depends(get_db),
):
    access_token, refresh_token, jti = tokens

    # Redirects user to profile
    response = RedirectResponse(url="/clinet/profile", status_code=303)

    # Sets tokens in cookies
    response.set_cookie(
        "access_token",
        access_token,
        httponly=True,
        secure=True,
        samesite=True,
        max_age=settings.JWT_EXPIRATION_MINUTES * 60,
        path="/",
    )
    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        secure=True,
        samesite=True,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
        patth="/",
    )
    expires_at = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    store_refresh_token(db, refresh_token, user.id, jti, expires_at)

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
