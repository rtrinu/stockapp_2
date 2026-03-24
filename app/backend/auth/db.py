from backend.core.hashing import hash_token
from backend.models.models import RefreshToken


def store_refresh_token(db, token: str, user_id: str, jti: str, expires_at):
    hashed = hash_token(token)
    db.add(
        RefreshToken(
            id=jti, user_id=user_id, hashed_token=hashed, expires_at=expires_at
        )
    )
    db.commit()


def create_user(
    db: Session,
    first_name: str,
    last_name: str,
    email: str,
    password: str,
    api_key: str,
    api_secret: str,
) -> User:
    created_at = datetime.now(timezone.utc)
    new_user = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        hashed_password=password,
        encrypted_api_key=api_key,
        encrypted_secret_key=api_secret,
        created_at=created_at,
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
