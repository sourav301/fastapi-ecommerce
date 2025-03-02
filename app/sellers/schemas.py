from pydantic import BaseModel
from typing import Optional

class ProductSeller(BaseModel):
    product_id: int
    seller_id: int
    price: float

class Seller(BaseModel):
    name: str
    contact: Optional[str]
    latitude: float
    longitude: float


class SellerResponse(Seller):
    id: int 
