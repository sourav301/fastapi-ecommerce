from fastapi import FastAPI
from app.routers import product
from app.core.database import engine, Base

app = FastAPI()

# Include routers
app.include_router(product.router)

# Create database tables (Run Alembic migrations instead in production)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup():
    await init_db()
