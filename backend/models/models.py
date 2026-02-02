from sqlmodel import Field, SQLModel, Column, DateTime, func
from datetime import datetime
import uuid
from typing import Optional


class Base(SQLModel):
    __abstract__ = True

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
    )


class User(Base, table=True):
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    # is_active: bool = Field(default=True)
    encrypted_api_key: Optional[str] = None
    encrypted_secret_key: Optional[str] = None
