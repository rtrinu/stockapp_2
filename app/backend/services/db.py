from sqlmodel import select, Session
from backend.models.models import Order, InternalOrderStatus


def get_order_from_db(db: Session, client_order_id: str) -> Order:
    statement = select(Order).where(Order.client_order_id == client_order_id)
    result = db.exec(statement).first()
    return result


def list_orders_from_db(db: Session, status: InternalOrderStatus) -> List[Order]:
    statement = select(Order).where(Order.status == status)
    result = db.exec(statement).all()
    return result


def check_order_duplicate(db: Session, client_order_id: str) -> bool:
    statement = select(Order).where(Order.client_order_id == client_order_id)
    order = db.exec(statement).first()
    if order:
        return True
    else:
        return False
