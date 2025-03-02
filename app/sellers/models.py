
from sqlalchemy import Column, String, Integer, DateTime, Float, func, ForeignKey
from sqlalchemy.orm import Session, relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base
from geoalchemy2 import Geometry

class ProductSellerModel(Base):
    __tablename__ = "product_sellers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    seller_id = Column(Integer, ForeignKey("sellers.id"))
    price = Column(Float, nullable=False)  # Seller-specific price for the product

    product = relationship("ProductModel", back_populates="sellers")
    seller = relationship("SellerModel", back_populates="products")

class SellerModel(Base):
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    contact = Column(String)
    address = Column(String)
    
    coordinates = Column(Geometry("POINT"))  # Stores longitude & latitude
    
    # Relationship to products
    products = relationship("ProductSellerModel", back_populates="seller")

