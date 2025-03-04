from .schemas import Order, OrderResponse
from .models import OrderModel
from .services import add_order
from fastapi import APIRouter, Depends
from app.database import get_db
from sqlalchemy.orm import Session


router = APIRouter()

@router.post("/orders/add", response_model=OrderResponse)
def order_add_api(order: Order, db: Session = Depends(get_db)):
    return add_order(OrderModel(**order.model_dump()), db)
