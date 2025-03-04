from .models import OrderModel
from sqlalchemy.orm import Session

def add_order(order: OrderModel, db: Session):
    db.add(order)
    db.commit()
    db.refresh(order)
    return order