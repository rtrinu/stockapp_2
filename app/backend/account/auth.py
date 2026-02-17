from backend.models.models import User
from sqlmodel import Session


def signup(
    db: Session, email: str, password: str, api_key: str, api_secret: str
) -> User:
    new_user = User(
        email=email,
        hashed_password=password,
        encrypted_secret_key=api_secret,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
