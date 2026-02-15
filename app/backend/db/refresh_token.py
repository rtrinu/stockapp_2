from sqlmodel import Session
from datetime import datetime
from uuid import UUID
from backend.core.hashing import hash_token
from backend.models.models import RefreshToken


def store_refresh_token(
    db: Session,
    raw_refresh_token: str,
    user_id: UUID,
    jti: str,
    expires_at: datetime,
) -> RefreshToken:

    token_hash = hash_token(raw_refresh_token)
    db_token = RefreshToken(
        user_id=user_id,
        jti=jti,
        token_hash=token_hash,
        created_at=datetime.utcnow(),
        expires_at=expires_at,
        revoked=False,
    )

    db.add(db_token)
    db.commit()
    db.refresh(db_token)

    return db_token
