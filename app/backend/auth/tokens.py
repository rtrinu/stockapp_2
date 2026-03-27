from datetime import datetime, timedelta, timezone
from backend.core.settings import settings
from backend.models.models import User
from uuid import uuid4
import jwt
from typing import Tuple, Optional, Dict


def create_access_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.JWT_EXPIRATION_MINUTES
    )

    payload = {"sub": user_id, "type": "access", "exp": expire}

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(user_id: str, jti: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    payload = {"sub": user_id, "jti": jti, "type": "refresh", "exp": expire}

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def generate_tokens(user: User) -> Tuple[str, str, str]:
    access_token = create_access_token(str(user.id))
    jti = str(uuid4())
    refresh_token = create_refresh_token(str(user.id), jti)
    return access_token, refresh_token, jti


def decode_jwt(token: str) -> Optional[Dict]:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={"require": ["sub", "exp"]},
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def is_token_not_expired(token_str: str) -> bool:
    try:
        # Attempt to decode and validate exp automatically
        jwt.decode(
            token_str,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            options={"verify_exp": True},
        )
        return True
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
