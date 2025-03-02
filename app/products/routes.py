from fastapi import APIRouter,  Depends, Form, File, UploadFile 
from app.database import Base, engine, get_db
from sqlalchemy.orm import relationship, Session 
from .schemas import Product
from .services import add_product, get_products
from typing import List 


router = APIRouter()

@router.get('/products/', response_model = list[Product])
def get_products_api(db: Session = Depends(get_db)):
    return get_products(db)
    
 
@router.post("/products/add", response_model=Product)
async def add_product_api(name: str = Form(...),
            desc: str = Form(None),
            category: str = Form(None),
            images: List[UploadFile] = File(...),
            db: Session = Depends(get_db)):
    
    return await add_product(name,desc,category,images,db)