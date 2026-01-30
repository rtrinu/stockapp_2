from models.models import TestUser
from sqlmodel import Session


def signup(
    db: Session, email: str, password: str, api_key: str, api_secret: str
) -> TestUser:
    new_user = TestUser(
        email=email,
        password=password,
        api_key=api_key,
        api_secret=api_secret,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
