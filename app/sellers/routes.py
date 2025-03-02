from .services import add_seller, add_product_seller, get_sellers
from fastapi import APIRouter, Depends
from app.database import Base, engine, get_db
from sqlalchemy.orm import relationship, Session 
from .schemas import Seller, ProductSeller, SellerResponse 

router = APIRouter()

@router.get("/sellers/", response_model=list[SellerResponse])
def get_sellers_api(db: Session = Depends(get_db) ):
    return get_sellers(db)

@router.post("/sellers/add", response_model=SellerResponse)
def add_seller_api(seller: Seller, db: Session = Depends(get_db)):
    seller_create = add_seller(seller,db)
    return SellerResponse(id=seller_create.id, **seller.model_dump())

@router.post("/product-sellers/", response_model=dict)
def add_product_seller_api(data: ProductSeller, db: Session = Depends(get_db)):
    add_product_seller(data, db)
    return {"message": "Product linked to seller successfully"}
