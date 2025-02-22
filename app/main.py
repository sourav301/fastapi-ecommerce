from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import engine, Base

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic (like initializing DB)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield  # Run the application

    # Shutdown logic (like closing DB connections)
    await engine.dispose()

# Initialize FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

# Import and include routes
from app.routers import product
app.include_router(product.router)
