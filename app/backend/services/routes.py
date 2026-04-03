from fastapi import APIRouter, Depends, Request
from backend.services.dependencies import get_alpaca_service
from backend.db.database import get_db
from backend.services.alpacaService import AlpacaService
from backend.models.models import InternalOrderStatus, Order
from backend.services.schema import OrderRead, OrderCreate
from backend.services.db import create_order_service
from sqlmodel import Session


router = APIRouter(tags=["service"])


@router.get("/account")
def get_user_account(service: AlpacaService = Depends(get_alpaca_service)):
    return service.get_account_info()


@router.get("/portfolio/value")
def get_user_portfolio(service: AlpacaService = Depends(get_alpaca_service)):
    # wraps get_portfolio
    return service.get_portfolio_value()


@router.get("/portfolio/history")
def get_user_portfolio_value(service: AlpacaService = Depends(get_alpaca_service)):
    # wraps get_portfolio_history
    return service.get_portfolio_history()


@router.get("/account/buying-power")
def get_user_buying_power(service: AlpacaService = Depends(get_alpaca_service)):
    # wraps get_buying_power
    return service.get_buying_power()


@router.get("/account/status")
def get_user_account_status(service: AlpacaService = Depends(get_alpaca_service)):
    # include trading_blocked, buying_power, portfolio_value
    return {
        "trading blocked": service.is_trading_blocked,
        "buying power": service.get_buying_power,
        "portfolio_value": service.get_portfolio_value,
    }


@router.post("/orders", response_model=OrderRead)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order_service(order, db)


@router.get("/orders")
# wraps get_orders
def get_user_orders(
    service: AlpacaService = Depends(get_alpaca_service), db: Session = Depends(get_db)
):
    return service.get_orders(db)


@router.get("/orders/{id}")
# wraps get_order
def get_user_order_by_id(
    id: str,
    service: AlpacaService = Depends(get_alpaca_service),
    db: Session = Depends(get_db),
):
    return service.get_order(id, db)


@router.get("/orders?status={status}")
# wraps list_orders_by_status
def list_user_orders_by_status(
    status: InternalOrderStatus,
    service: AlpacaService = Depends(get_alpaca_service),
    db: Session = Depends(get_db),
):
    return service.list_orders_by_status(status, db)


# @router.post("/orders/{id}/cancel")
# #wraps cancel_order and updates db status

# @router.post("/orders/cancel-all")
# #wraps cancel_all_orders


@router.get("/positions")
# wraps get_positions
def get_user_positions(
    service: AlpacaService = Depends(get_alpaca_service), db: Session = Depends(get_db)
):
    return service.get_positions(db)


@router.get("/positions/{symbol}")
# wraps get_position
def get_user_position(
    symbol: str,
    service: AlpacaService = Depends(get_alpaca_service),
    db: Session = Depends(get_db),
):
    return service.get_position(symbol, db)


# @router.get("/positions/{symbol}/close")
# #wraps close_position


# @router.get("/positions/close-all")
# #wraps close_all_positions


@router.get("/assets/{symbol}")
# wraps get_asset
def get_user_asset(symbol: str, service: AlpacaService = Depends(get_alpaca_service)):
    return service.get_asset(symbol)


@router.get("/assets/{symbol}/tradable")
# wraps is_tradable
def is_tradable(symbol: str, service: AlpacaService = Depends(get_alpaca_service)):
    return service.is_tradable(symbol)
