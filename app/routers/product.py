from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.product import ProductCreate, ProductResponse
from app.crud.product import create_product

router = APIRouter()

@router.post("/products/", response_model=ProductResponse)
async def add_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await create_product(db, product)
