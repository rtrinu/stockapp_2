from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest
from alpaca.trading.requests import GetAssetsRequest
from backend.models.models import User
from backend.core.cryptography import decrypt


class AlpacaService:
    def __init__(self, user):
        self.client = TradingClient(
            decrypt(user.encrypted_api_key),
            decrypt(user.encrypted_api_secret),
            paper=True,
        )

    def get_account_info(self):
        return self.client.get_account()

    def get_buying_power(self):
        account = self.get_account_info()
        return account.buying_power

    def is_trading_blocked(self):
        account = self.get_account_info()
        return account.trading_blocked

    def place_market_order(self, symbol: str, qty: float, side, timeInForce=None):
        market_order_data = MarketOrderRequest(
            symbol=symbol, qty=qty, side=side, time_in_force=timeInForce
        )
        market_order = self.client.submit_order(order_data=market_order_data)
        return {"order": "submitted", "data": market_order_data}

    def place_limit_order(
        self, symbol: str, qty: float, limit_price: float, side, timeInForce=None
    ):
        limit_order_data = LimitOrderRequest(
            symbol=symbol,
            qty=qty,
            limit_price=limit_price,
            side=side,
            time_in_force=timeInForce,
        )
        limit_order = self.client.submit_order(order_data=limit_order_data)
        return {"order": "submitted", "data": limit_order_data}

    def place_stop_order(self):
        pass

    def get_order(order_id):
        pass

    def list_orders(status):
        pass

    def cancel_order(order_id):
        pass

    def cancel_all_orders():
        pass

    def get_positions():
        pass

    def get_position(symbol: str):
        pass

    def close_position(symbol: str):
        pass

    def close_all_positions():
        pass

    def get_portfolio_value():
        pass

    def get_portfolio_history():
        pass

    def is_tradable(symbol: str):
        pass

    def get_asset(symbol: str):
        pass

    def validate_order(symbol: str, qty: int):
        pass

    def check_risk_limits():
        pass

    def prevent_duplicate_orders(order_id):
        pass
