from fastapi import APIRouter

import app.products.routes as product_routes
import app.sellers.routes as seller_routes
import app.orders.routes as order_routes

router = APIRouter()

router.include_router(product_routes.router, tags=["Products"])
router.include_router(seller_routes.router, tags=["Sellers"])
router.include_router(order_routes.router, tags=["Orders"])