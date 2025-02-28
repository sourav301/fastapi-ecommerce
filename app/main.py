from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional

from .database import Base, engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from sqlalchemy import Column, String, Integer

app = FastAPI(swagger_ui_parameters={"theme": "dark"})


class Product(BaseModel):
    id: int = 0
    name: str
    desc: Optional[str] = None  # Optional field with a default value
    
    class Config:
        from_attributes = True 

class  ProductModel(Base):
    __tablename__= "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    desc = Column(String)
 
 
@app.get('/products/', response_model = list[Product])
def get_products(db: Session = Depends(get_db)):
    return db.query(ProductModel).all()

@app.post("/products/add", response_model=Product)
def add_product(product: Product, db: Session = Depends(get_db)):
    productModel = ProductModel(**product.model_dump())
    db.add(productModel)
    db.commit()
    db.refresh(productModel)
    return productModel

