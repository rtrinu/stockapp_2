from sqlmodel import SQLModel
from typing import Optional
from backend.models.models import OrderBase
from uuid import UUID
import uuid


class OrderCreate(SQLModel):
    symbol: str
    qty: float
    type: str
    side: str

    time_in_force: str
    user_id: UUID
    alpaca_order_id: str

    limit_price: Optional[float] = None
    stop_price: Optional[float] = None


class OrderRead(OrderBase):
    id: uuid.UUID
