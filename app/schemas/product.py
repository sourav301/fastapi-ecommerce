from typing import Optional
from pydantic import BaseModel

class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class CategoryResponse(CategoryCreate):
    id: int
    name: str

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    name: str
    category_id: int
    description:  Optional[str] = None 
    price: float
    stock: int

class ProductRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    category: CategoryRead 

    class Config:
        from_attributes = True

class ProductResponse(ProductCreate):
    id: int

    class Config:
        from_attributes = True






