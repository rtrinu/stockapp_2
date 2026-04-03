from sqlmodel import select, Session
from backend.models.models import Order, InternalOrderStatus, Position

# from backend.services.dependencies import map_raw_to_internal_status
from backend.services.schema import OrderCreate
from uuid import UUID
from typing import Dict
from datetime import datetime, timezone


def create_order_service(order_data: OrderCreate, db: Session) -> Order:
    db_order = Order.model_validate(order_data)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


# def store_order(db: Session, user_id: UUID, alpaca_order):
#     existing = check_order_duplicate(db, alpaca_order.id)
#     if existing:
#         order = existing
#     else:
#         order = Order(
#             user_id=user_id,
#             alpaca_order_id=alpaca_order.id,
#             created_at=datetime.now(timezone.utc),
#         )
#     order.symbol = alpaca_order.symbol
#     order.qty = float(alpaca_order.qty)
#     order.side = alpaca_order.side
#     order.order_type = alpaca_order.order_type
#     order.limit_price = getattr(alpaca_order, "limit_price", None)
#     order.stop_price = getattr(alpaca_order, "stop_price", None)

#     order.alpaca_status = alpaca_order.status
#     order.status = map_raw_to_internal_status(alpaca_order.status)

#     order.client_order_id = alpaca_order.client_order_id

#     order.updated_at = datetime.now(timezone.utc)

#     db.add(order)
#     db.commit()
#     db.refresh(order)

#     return order


# def update_order_in_db(db: Session, order_id: str, changes: Dict[str:object]) -> Order:
#     statement = select(Order).where(Order.alpaca_order_id == order_id)
#     order = db.exec(statement).first()

#     if not order:
#         raise ValueError("Order not found")

#     for field, value in changes.items():
#         setattr(order, field, value)

#     db.add(order)
#     db.commit()
#     db.refresh(existing)

#     return order


# def store_position():
#     pass


# def get_orders(user_id: UUID, db: Session) -> List[Order]:
#     statement = select(Order).where(Order.user_id == user_id)
#     result = db.exec(statement).all()
#     return result


# def get_order_from_db(user_id: UUID, db: Session, client_order_id: str) -> Order:
#     statement = (
#         select(Order)
#         .where(Order.client_order_id == client_order_id)
#         .where(Order.user_id == user_id)
#     )
#     result = db.exec(statement).first()
#     return result


# def list_orders_from_db(db: Session, status: InternalOrderStatus) -> List[Order]:
#     statement = (
#         select(Order).where(Order.status == status).where(Order.user_id == user_id)
#     )
#     result = db.exec(statement).all()
#     return result


# def check_order_duplicate(db: Session, client_order_id: str) -> bool:
#     statement = (
#         select(Order)
#         .where(Order.client_order_id == client_order_id)
#         .where(Order.user_id == user_id)
#     )
#     order = db.exec(statement).first()
#     if order:
#         return True
#     else:
#         return False


# def get_position_from_db(db: Session, user_id: UUID, symbol: str) -> Position:
#     statement = (
#         select(Position)
#         .where(Position.user_id == user_id)
#         .where(Position.symbol == symbol)
#     )
#     position = db.exec(statement).first()
#     return position


# def get_all_positions(db: Session, user_id: UUID) -> List[Position]:
#     statement = select(Position).where(Position.user_id == user_id)
#     positions = db.exec(statement).all()
#     return positions
