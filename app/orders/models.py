from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)  # ForeignKey for product
    price = Column(Integer, nullable=False)
    desc = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    
    product = relationship("ProductModel", back_populates="orders")
