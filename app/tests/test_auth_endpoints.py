# tests/test_auth_endpoints.py

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool

from main import app
from backend.db.database import get_db

# ——————————————— Setup in‑memory test DB ————————————————
TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


# ——————————————— Tests ————————————————


def test_signup_creates_user(client):
    response = client.post(
        "/auth/sign-up",
        data={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "wrongpass@example.com",
            "password": "RightPass!",
            "client_key": "a",
            "client_secret": "b",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    assert body["email"] == "user1@example.com"


def test_signup_duplicate_email(client):
    payload = {
        "first_name": "john",
        "last_name": "doe",
        "email": "dup@example.com",
        "password": "pass",
        "client_key": "k",
        "client_secret": "s",
    }
    r1 = client.post("/auth/sign-up", data=payload)
    assert r1.status_code == 201

    r2 = client.post("/auth/sign-up", data=payload)
    assert r2.status_code == 400
    assert "User already exists" in r2.json()["detail"]


def test_login_succeeds(client):
    signup_data = {
        "email": "loginok@example.com",
        "password": "Correct123!",
        "client_key": "keyX",
        "client_secret": "secretX",
    }
    assert client.post("/auth/sign-up", data=signup_data).status_code == 201

    login_data = {
        "email": "loginok@example.com",
        "password": "Correct123!",
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 201

    body = response.json()
    assert "access_token" in body
    assert isinstance(body["access_token"], str)


def test_login_wrong_password(client):
    client.post(
        "/auth/sign-up",
        data={
            "email": "wrongpass@example.com",
            "password": "RightPass!",
            "client_key": "a",
            "client_secret": "b",
        },
    )
    bad_login = {
        "email": "wrongpass@example.com",
        "password": "WrongPass!",
    }
    response = client.post("/auth/login", data=bad_login)
    assert response.status_code == 401
    assert "Invalid password" in response.json()["detail"]


def test_login_user_not_found(client):
    response = client.post(
        "/auth/login",
        data={
            "email": "notfound@example.com",
            "password": "anything",
        },
    )
    assert response.status_code == 400
    assert "User not found" in response.json()["detail"]
