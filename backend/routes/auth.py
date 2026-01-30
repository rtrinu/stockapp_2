from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from db.database import get_db
from models.models import TestUser
from core.settings import settings
from core.cryptography import encrypt, decrypt
from account.auth import signup
from pwdlib import PasswordHash

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
    existing = db.query(TestUser).filter(TestUser.email == email).first()
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
    email: str,
    password: str,
    db: Session = Depends(get_db),
):
    existing = db.query(TestUser).filter(TestUser.email == email).first()
    if not existing:
        raise HTTPException(status_code=400, detail="User not found")
    verify_password = hasher.verify(password, existing.password)
    if verify_password:
        return {"id": existing.id, "email": existing.email}
    else:
        raise HTTPException(status_code=401, detail="Invalid password")
