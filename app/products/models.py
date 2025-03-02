
from sqlalchemy import Column, String, Integer, DateTime, Float, func, ForeignKey
from sqlalchemy.orm import Session, relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base

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
 