from sqlmodel import Field, SQLModel, Column, Relationship
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime, timezone
import uuid
from typing import Optional, List, Dict


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

    encrypted_api_key: Optional[str] = None
    encrypted_secret_key: Optional[str] = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    refresh_tokens: List["RefreshToken"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    orders: List["Order"] = Relationship(back_populates="user")
    positions: List["Position"] = Relationship(back_populates="user")


class RefreshToken(Base, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, index=True)

    token_hash: str = Field(nullable=False)
    expires_at: datetime = Field(nullable=False)
    revoked: bool = Field(default=False)

    user: User = Relationship(back_populates="refresh_tokens")


class InternalOrderStatus(str):
    PENDING = "pending"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELED = "canceled"
    FAILED = "failed"


class OrderType(str):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"


class OrderSide(str):
    BUY = "buy"
    SELL = "sell"


class Order(Base, table=True):
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)

    symbol: str
    qty: float

    side: str
    order_type: str

    status: str = Field(default=InternalOrderStatus.PENDING)

    details: Optional[dict] = Field(default=None, sa_column=Column(JSONB))

    alpaca_order_id: Optional[str] = Field(default=None, index=True)
    client_order_id: Optional[str] = Field(default=None, index=True)
    alpaca_status: Optional[str] = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    user: Optional["User"] = Relationship(back_populates="orders")


class Position(Base, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)

    symbol: str = Field(index=True)
    qty: float
    avg_entry_price: float

    market_value: Optional[float] = None
    unrealised_pl: Optional[float] = None

    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    user: Optional["User"] = Relationship(back_populates="positions")
