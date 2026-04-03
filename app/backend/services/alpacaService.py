from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest, OrderRequest
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import OrderSide, OrderType, TimeInForce
from backend.models.models import User, InternalOrderStatus, Position
from backend.core.cryptography import decrypt
from sqlmodel import Session

# from backend.services.db import (
#     get_order_from_db,
#     list_orders_from_db,
#     check_order_duplicate,
#     get_orders,
#     get_all_positions,
#     get_position_from_db,
# )
from typing import Optional, Sequence, List
from backend.models.models import Order


class AlpacaService:
    def __init__(self, user) -> None:
        self.client = TradingClient(
            decrypt(user.encrypted_api_key),
            decrypt(user.encrypted_api_secret),
            paper=True,
        )
        self.user = user

    def get_account_info(self) -> object:
        return self.client.get_account()

    def get_buying_power(self) -> float:
        account = self.get_account_info()
        return account.buying_power

    def is_trading_blocked(self) -> bool:
        account = self.get_account_info()
        return account.trading_blocked

    def create_market_order(self, symbol: str, qty: float, side: OrderSide):
        return MarketOrderRequest(
            symbol=symbol,
            qty=qty,
            side=side,
            time_in_force=TimeInForce.DAY,
            order_type=OrderType.MARKET,
        )

    def create_limit_order(
        self, symbol: str, qty: float, limit_price: float, side: OrderSide
    ):
        return LimitOrderRequest(
            symbol=symbol,
            qty=qty,
            limit_price=limit_price,
            side=side,
            time_in_force=timeInForce.DAY,
            order_type=OrderType.LIMIT,
        )

    def create_stop_order(
        self, symbol: str, qty: float, side: OrderSide, stop_price: float
    ) -> OrderRequest:
        return OrderRequest(
            symbol=symbol,
            qty=qty,
            side=side,
            order_type=OrderType.STOP,
            stop_price=stop_price,
            time_in_force=TimeInForce.DAY,
        )

    def submit_order(self, order_data) -> object:
        return self.client.submit_order(order_data)

    def get_order(self, order_id: str, db: Session) -> Order:
        order = get_order_from_db(db, order_id, self.user.id)
        if not order:
            raise ValueError("Order not Found")
        return order

    def get_orders(self, db: Session) -> List[Order]:
        orders = get_orders(self.user.id, db)
        if not orders:
            raise ValueError("Orders not Found")
        return orders

    def list_orders_by_status(
        self, status: InternalOrderStatus, db: Session
    ) -> List[Order]:
        orders = list_orders_from_db(db, status)
        if not orders:
            raise Value("Orders not Found")
        return orders

    def cancel_order(self, order_id: str) -> object:
        return self.client.cancel_order_by_id(order_id)

    def cancel_all_orders(self) -> List[object]:
        return self.client.cancel_orders()

    def get_positions(self, db: Session) -> List[Position]:
        return get_all_positions(self.user.id, db)

    def get_position(self, symbol: str, db: Session) -> Position:
        return get_position_from_db(self.user.id, symbol, db)

    def close_position(self, symbol: str) -> object:
        return self.client.close_position(symbol)

    def close_all_positions(self) -> Sequence[object]:
        return self.client.close_all_positions()

    def get_portfolio_value(self) -> float:
        account = self.get_account_info()
        return account.portfolio_value

    def get_portfolio_history(self) -> object:
        return self.client.get_portfolio_history()

    def is_tradable(self, symbol: str) -> bool:
        asset = self.client.get_asset(symbol)
        return asset.tradable

    def get_asset(self, symbol: str) -> object:
        return self.client.get_asset(symbol)

    def validate_order(self, symbol: str, qty: int) -> bool:
        if qty <= 0:
            return False, "Quantity must be greater than zero."
        try:
            asset = self.get_asset(symbol)
        except Exception:
            return False, f"Symbol {symbol} not found"
        if not self.is_tradable(symbol):
            return False, f"{symbol} is not tradable on Alpaca"
        try:
            buying_power = self.get_buying_power()
        except Exception:
            buying_power = 0

        return True, ""

    def check_risk_limits():
        pass

    def prevent_duplicate_orders(order_id: str) -> bool:
        return check_order_duplicate(order_id)
