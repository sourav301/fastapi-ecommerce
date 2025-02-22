from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.product import ProductCreate, ProductResponse, CategoryCreate, CategoryResponse
from app.crud.product import create_product, create_category, get_products
from app.schemas.product import ProductRead 
from typing import List

router = APIRouter()

@router.get("/products", response_model=List[ProductRead])
async def list_products(db: AsyncSession = Depends(get_db)):
    products = await get_products(db)
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    return products

@router.post("/products/", response_model=ProductResponse)
async def add_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await create_product(db, product)

@router.post("/categories/", response_model=CategoryResponse)
async def add_category(category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    return await create_category(db, category)
