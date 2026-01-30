from models.models import TestUser


def signup(email: str, password: str, api_key: str, api_secret: str) -> User:
    new_user = TestUser(
        email,
        password,
        api_key,
    )
    return new_user
