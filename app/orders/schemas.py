from pydantic import BaseModel
from typing import Optional

class Order(BaseModel):
    customer_id: int
    product_id: int
    price: int
    desc: Optional[str]

class OrderResponse(Order):
    id: int