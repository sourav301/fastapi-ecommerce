from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product, Category
from app.schemas.product import ProductCreate, CategoryCreate
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select

async def create_product(db: AsyncSession, product: ProductCreate):
    db_product = Product(
        name=product.name,
        category_id=product.category_id,
        description=product.description,
        price=product.price,
        stock=product.stock
    )
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def create_category(db: AsyncSession, category: CategoryCreate):
    db_category = Category(
        name=category.name,
        description=category.description
    )
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

async def get_products(db: AsyncSession):
    result = await db.execute(select(Product).options(selectinload(Product.category)))
    return result.scalars().all()