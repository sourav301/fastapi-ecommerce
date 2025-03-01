from fastapi import FastAPI, Depends, File, UploadFile, Form
from pydantic import BaseModel, conlist
from typing import Optional, List

from .database import Base, engine, SessionLocal, get_db
from sqlalchemy.orm import Session, relationship
from sqlalchemy import Column, String, Integer, DateTime, Float, func, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from geoalchemy2 import Geometry
from geoalchemy2 import WKTElement
import os

from datetime import datetime

app = FastAPI(swagger_ui_parameters={"theme": "dark"})


class Product(BaseModel):
    id: int = 0
    name: str
    desc: Optional[str] = None  # Optional field with a default value
    created_at: Optional[datetime] = None
    category: Optional[str] = None
    images: List[str]
    class Config:
        from_attributes = True 

class ProductSeller(BaseModel):
    product_id: int
    seller_id: int
    price: float

class Seller(BaseModel):
    name: str
    contact: Optional[str]
    latitude: float
    longitude: float

    

class ProductModel(Base):
    __tablename__= "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    desc = Column(String)
    category = Column(String)
    images = Column(JSONB, nullable=True)# Relationship to sellers
    sellers = relationship("ProductSellerModel", back_populates="product")
    created_at = Column(DateTime, nullable=True, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, server_default=func.now())
 
class SellerModel(Base):
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    contact = Column(String)
    address = Column(String)
    
    coordinates = Column(Geometry("POINT"))  # Stores longitude & latitude
    
    # Relationship to products
    products = relationship("ProductSellerModel", back_populates="seller")

class ProductSellerModel(Base):
    __tablename__ = "product_sellers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    seller_id = Column(Integer, ForeignKey("sellers.id"))
    price = Column(Float, nullable=False)  # Seller-specific price for the product

    product = relationship("ProductModel", back_populates="sellers")
    seller = relationship("SellerModel", back_populates="products")

Base.metadata.create_all(bind = engine)
@app.get('/products/', response_model = list[Product])
def get_products(db: Session = Depends(get_db)):
    return db.query(ProductModel).all()


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
@app.post("/products/add", response_model=Product)
async def add_product(name: str = Form(...),
            desc: str = Form(None),
            category: str = Form(None),
            images: List[UploadFile] = File(...),
            db: Session = Depends(get_db)):
    
    image_urls = []
    
    for image in images:
        file_location = os.path.join(UPLOAD_DIR, image.filename)
        with open(file_location, "wb") as buffer:
            buffer.write(await image.read())  # Save image file

        image_url = f"/static/{image.filename}"  # URL to access the image
        image_urls.append(image_url)

    new_product = ProductModel(
        name=name,
        desc=desc,
        category=category,
        images=image_urls
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.post("/sellers/add", response_model=Seller)
def add_seller(seller: Seller, db: Session = Depends(get_db)):
    coordinates = WKTElement(f"POINT({seller.longitude} {seller.latitude})", srid=4326)

    
    seller_db = SellerModel(
        name=seller.name,
        contact=seller.contact,
        coordinates=coordinates,  # Convert lat/lon to PostGIS format
    )
    db.add(seller_db)
    db.commit()
    db.refresh(seller_db)  # Fetch the latest data from DB
    return seller

@app.post("/product-sellers/", response_model=dict)
def add_product_seller(data: ProductSeller, db: Session = Depends(get_db)):
    product_seller = ProductSellerModel(
        product_id=data.product_id,
        seller_id=data.seller_id,
        price=data.price
    )
    db.add(product_seller)
    db.commit()
    return {"message": "Product linked to seller successfully"}