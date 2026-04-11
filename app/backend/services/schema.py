from pydantic import BaseModel, Field, model_validator
from typing import Optional, Dict, Any
from enum import Enum
import uuid
from datetime import datetime


class InternalOrderStatus(str, Enum):
    PENDING = "pending"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELED = "canceled"
    FAILED = "failed"


class OrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"


class OrderSide(str, Enum):
    BUY = "buy"
    SELL = "sell"


class OrderCreate(BaseModel):
    symbol: str
    qty: float
    side: OrderSide
    order_type: OrderType
    details: Optional[Dict[str, Any]] = None

    @model_validator(mode="before")
    @classmethod
    def validate_details(cls, values):
        if not isinstance(values, dict):
            return values  # let pydantic handle it

        order_type = values.get("order_type")
        details = values.get("details") or {}

        if order_type == OrderType.MARKET:
            if details:
                raise ValueError("Market orders must not include details")

        if order_type == OrderType.LIMIT:
            if "limit_price" not in details:
                raise ValueError("Limit order requires limit_price")

        if order_type == OrderType.STOP:
            if "stop_price" not in details:
                raise ValueError("Stop order requires stop_price")

        if order_type == OrderType.STOP_LIMIT:
            if "stop_price" not in details or "limit_price" not in details:
                raise ValueError("Stop-limit requires stop_price + limit_price")

        return values


class OrderRead(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    symbol: str
    qty: float
    side: OrderSide
    order_type: OrderType
    status: InternalOrderStatus
    details: Optional[Dict[str, Any]]
    alpaca_order_id: Optional[str]
    client_order_id: Optional[str]
    alpaca_status: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
