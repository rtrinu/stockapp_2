from fastapi import APIRouter, Depends, Request
from backend.services.tradingClient import get_alpaca_client
from backend.auth.dependencies import get_current_user
from backend.db.database import get_db
from backend.services.alpacaService import AlpacaService
from backend.models.models import InternalOrderStatus
from sqlModel import Session


router = APIRouter(tags=["client"])


@router.get("/get-client")
def get_alpaca_client(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    client = AlpacaService(user)
    return client


@router.get("/account")
def get_user_account(client: AlpacaService):
    return client.get_account_info()


@router.get("/portfolio/value")
def get_user_portfolio(client: AlpacaService):
    # wraps get_portfolio
    return client.get_portfolio_value()


@router.get("/portfolio/history")
def get_user_portfolio_value(client: AlpacaService):
    # wraps get_portfolio_history
    return client.get_portfolio_history()


@router.get("/account/buying-power")
def get_user_buying_power(client: AlpacaService):
    # wraps get_buying_power
    return client.get_buying_power()


@router.get("/account/status")
def get_user_account_status(client: AlpacaService):
    # include trading_blocked, buying_power, portfolio_value
    return {
        "trading blocked": client.is_trading_blocked,
        "buying power": client.get_buying_power,
        "portfolio_value": client.get_portfolio_value,
    }


# @router.post("/orders")


@router.get("/orders")
# wraps get_orders
def get_user_orders(client: AlpacaService, db: Session = Depends(get_db)):
    return client.get_orders(db)


@router.get("/orders/{id}")
# wraps get_order
def get_user_order_by_id(client: AlpacaService, id: str, db: Session = Depends(get_db)):
    return client.get_order(id, db)


@router.get("/orders?status={status}")
# wraps list_orders_by_status
def list_user_orders_by_status(
    client: AlpacaService, status: InternalOrderStatus, db: Session = Depends(get_db)
):
    return client.list_orders_by_status(status, db)


# @router.post("/orders/{id}/cancel")
# #wraps cancel_order and updates db status

# @router.post("/orders/cancel-all")
# #wraps cancel_all_orders


@router.get("/positions")
# wraps get_positions
def get_user_positions(client: AlpacaService, db: Session = Depends(get_db)):
    return client.get_positions(db)


@router.get("/positions/{symbol}")
# wraps get_position
def get_user_position(
    client: AlpacaService, symbol: str, db: Session = Depends(get_db)
):
    return client.get_position(symbol, db)


# @router.get("/positions/{symbol}/close")
# #wraps close_position


# @router.get("/positions/close-all")
# #wraps close_all_positions


@router.get("/assets/{symbol}")
# wraps get_asset
def get_user_asset(client: AlpacaService, symbol: str):
    return client.get_asset(symbol)


@router.get("/assets/{symbol}/tradable")
# wraps is_tradable
def is_tradable(client: AlpacaService, symbol: str):
    return client.is_tradable(symbol)
