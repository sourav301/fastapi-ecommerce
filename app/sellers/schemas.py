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


class CoordinatesSchema(BaseModel):
    latitude: float
    longitude: float

class SellerSchema(BaseModel):
    id: int
    name: str
    contact: Optional[str] = None 
    coordinates: Optional[CoordinatesSchema] = None  # Serialize coordinates properly

    class Config:
        from_attributes = True  # Allows automatic conversion from SQLAlchemy model