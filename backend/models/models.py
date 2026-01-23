from sqlmodel import Field, SQLModel, Column, DateTime, func
from datetime import datetime
import uuid
from typing import Optional


class TimestampModel(SQLModel):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False
    )
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
        )
    )


class User(TimestampModel, table=True):
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    encrypted_api_key: Optional[str] = None
    encrypted_secret_key: Optional[str] = None
