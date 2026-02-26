from backend.models.models import User
from sqlmodel import Session


def signup(
    db: Session,
    email: str,
    password: str,
    api_key: str,
    api_secret: str,
    hashed_secret_key: str,
) -> User:
    new_user = User(
        email=email,
        hashed_password=password,
        encrypted_api_key=api_key,
        encrypted_secret_key=api_secret,
        hashed_secret_key=hashed_secret_key,
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    except SQLAlchemyError as db_err:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Database error during signup: {str(db_err)}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Unexpected error during signup: {str(e)}"
        )
