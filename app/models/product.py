from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # ✅ Auto-set on insert
    modified_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())  # ✅ Auto-update on modification

    category = relationship("Category", back_populates="products")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True,nullable=False)
    description = Column(String, nullable=False)

    products = relationship("Product", back_populates="category")

    