# tests/test_auth_token.py
import pytest
from fastapi.testclient import TestClient
from main import app
from backend.db.database import get_db
from sqlmodel import Session, SQLModel, create_engine
from backend.models.models import User, RefreshToken
from backend.core.auth_handler import create_access_token, create_refresh_token
from datetime import datetime, timedelta, timezone
import jwt
from backend.core.settings import settings

# ---------- Set up test DB ----------
DATABASE_URL = "sqlite:///./test_token.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SQLModel.metadata.create_all(engine)


# Override get_db
def override_get_db():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture
def test_user():
    # Create a user directly in DB
    with Session(engine) as db:
        user = User(
            first_name="Alice",
            last_name="Smith",
            email="alice@example.com",
            hashed_password="hashedpassword",
            created_at=datetime.now(timezone.utc),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        yield user
        # cleanup
        db.delete(user)
        db.commit()


@pytest.fixture
def valid_tokens(test_user):
    access_token = create_access_token(str(test_user.id))
    jti = "test-jti"
    refresh_token = create_refresh_token(str(test_user.id), jti)
    # store refresh token in DB
    with Session(engine) as db:
        db.add(
            RefreshToken(
                user_id=test_user.id,
                jti=jti,
                token_hash=refresh_token,
                created_at=datetime.now(timezone.utc),
                expires_at=datetime.now(timezone.utc)
                + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            )
        )
        db.commit()
    return access_token, refresh_token


# ---------- Helper to call get_or_refresh_access_token ----------
from backend.routes.auth import get_or_refresh_access_token
from fastapi import Request, Response


class DummyRequest:
    def __init__(self, cookies):
        self.cookies = cookies


class DummyResponse:
    def __init__(self):
        self.cookies_set = {}

    def set_cookie(self, key, value, **kwargs):
        self.cookies_set[key] = value


def test_valid_access_token(test_user, valid_tokens):
    access_token, refresh_token = valid_tokens
    request = DummyRequest(cookies={"access_token": access_token})
    response = DummyResponse()
    token = get_or_refresh_access_token(request, response)
    assert token == access_token
    assert "access_token" not in response.cookies_set  # no new cookie needed


def test_expired_access_token_refresh(test_user, valid_tokens, monkeypatch):
    old_access, refresh_token = valid_tokens

    # create a token that is expired
    expired_payload = jwt.decode(
        old_access,
        settings.JWT_SECRET,
        algorithms=[settings.JWT_ALGORITHM],
        options={"verify_exp": False},
    )
    expired_payload["exp"] = (
        datetime.now(timezone.utc).timestamp() - 10
    )  # expired 10s ago
    expired_token = jwt.encode(
        expired_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )

    request = DummyRequest(
        cookies={"access_token": expired_token, "refresh_token": refresh_token}
    )
    response = DummyResponse()

    token = get_or_refresh_access_token(request, response)
    assert token != expired_token  # should be a new token
    assert "access_token" in response.cookies_set


def test_no_tokens_returns_none():
    request = DummyRequest(cookies={})
    response = DummyResponse()
    token = get_or_refresh_access_token(request, response)
    assert token is None
