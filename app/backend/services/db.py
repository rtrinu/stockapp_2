from sqlmodel import select, Session
from backend.models.models import Order, InternalOrderStatus, Position
from uuid import UUID


def get_orders(user_id: UUID, db: Session) -> List[Order]:
    statement = select(Order).where(Order.user_id == user_id)
    result = db.exec(statement).all()
    return result


def get_order_from_db(user_id: UUID, db: Session, client_order_id: str) -> Order:
    statement = (
        select(Order)
        .where(Order.client_order_id == client_order_id)
        .where(Order.user_id == user_id)
    )
    result = db.exec(statement).first()
    return result


def list_orders_from_db(db: Session, status: InternalOrderStatus) -> List[Order]:
    statement = (
        select(Order).where(Order.status == status).where(Order.user_id == user_id)
    )
    result = db.exec(statement).all()
    return result


def check_order_duplicate(db: Session, client_order_id: str) -> bool:
    statement = (
        select(Order)
        .where(Order.client_order_id == client_order_id)
        .where(Order.user_id == user_id)
    )
    order = db.exec(statement).first()
    if order:
        return True
    else:
        return False


def get_position_from_db(db: Session, user_id: UUID, symbol: str) -> Position:
    statement = (
        select(Position)
        .where(Position.user_id == user_id)
        .where(Position.symbol == symbol)
    )
    position = db.exec(statement).first()
    return position
