from sqlmodel import Field, SQLModel, Column, DateTime, func, Relationship
from datetime import datetime, timezone
import uuid
from typing import Optional, List


class Base(SQLModel):
    __abstract__ = True

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
    )


class User(Base, table=True):
    email: str = Field(unique=True, index=True, nullable=False)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    hashed_password: str = Field(nullable=False)
    # is_active: bool = Field(default=True)
    encrypted_api_key: Optional[str] = None
    encrypted_secret_key: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))

    refresh_tokens: List["RefreshToken"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class RefreshToken(Base, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, index=True)

    jti: str = Field(nullable=False, unique=True, index=True)
    token_hash: str = Field(nullable=False)

    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    last_used_at: datetime | None = Field(default=None)
    expires_at: datetime = Field(nullable=False)
    revoked: bool = Field(default=False)

    user: User = Relationship(back_populates="refresh_tokens")
