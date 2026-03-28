from sqlmodel import Field, SQLModel, Column, DateTime, func, Relationship
from datetime import datetime, timezone
from alpaca.trading.enums import OrderSide, OrderType, OrderStatus
import uuid
from typing import Optional, List
from datetime import datetime, timezone
from enum import Enum


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

    orders: List["Order"] = Relationship(back_populates="user")


class RefreshToken(Base, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, index=True)

    token_hash: str = Field(nullable=False)
    expires_at: datetime = Field(nullable=False)
    revoked: bool = Field(default=False)

    user: User = Relationship(back_populates="refresh_tokens")


class InternalOrderStatus(str, Enum):
    PENDING = "pending"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELED = "canceled"
    FAILED = "failed"


class Order(Base, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    alpaca_order_id: Optional[str] = Field(default=None, index=True)

    symbol: str = Field(index=True)
    qty: float
    side: OrderSide
    order_type: OrderType

    limit_price: Optional[float] = None
    stop_price: Optional[float] = None

    status: OrderStatus = Field(default=InternalOrderStatus.PENDING)

    alpaca_status: Optional[str] = None

    client_order_id: Optional[str] = Field(default=None, index=True)

    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=datetime.now(timezone.utc))

    user: Optional["User"] = Relationship(back_populates="orders")
