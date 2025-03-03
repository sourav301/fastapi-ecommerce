from fastapi import APIRouter,  Depends, Form, File, UploadFile 
from app.database import Base, engine, get_db
from sqlalchemy.orm import relationship, Session 
from .schemas import Product
from .services import add_product, get_products
from app.sellers.schemas import SellerResponse, Seller, SellerSchema, CoordinatesSchema
from app.sellers.models import SellerModel, ProductSellerModel
from geoalchemy2.functions import ST_Distance, ST_GeomFromText
from geoalchemy2.functions import ST_Distance, ST_SetSRID
from sqlalchemy import select, func, cast
from sqlalchemy.future import select
from typing import List 
from shapely.wkb import loads 
from geoalchemy2 import Geography


router = APIRouter()

@router.get('/products/', response_model = list[Product])
def get_products_api(db: Session = Depends(get_db)):
    return get_products(db)

@router.get('/products/{product_id}/sellers')
def get_products_api(product_id: int, 
                        latitude: float, 
                        longitude: float, 
                        db: Session = Depends(get_db)):
    user_location = ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326)

    point = f"POINT({longitude} {latitude})"
    query = (
        select(
            SellerModel, 
            ST_Distance(cast(SellerModel.coordinates,Geography), cast(user_location,Geography)).label("distance")
        ) 
        .join(ProductSellerModel, ProductSellerModel.seller_id == SellerModel.id)
        .where(ProductSellerModel.product_id == product_id)
        .order_by("distance")  # Optional: Sort by closest sellers
    )
    result = db.execute(query).all()  # Returns Row objects, not tuples

    seller_list = []
    for row in result:
        seller = row[0]  # Extract SellerModel
        distance = row.distance  # Extract distance

        coordinates = None
        if seller.coordinates:
            point = loads(bytes(seller.coordinates.data))  # Convert WKB to Shapely Point
            coordinates = CoordinatesSchema(latitude=point.y, longitude=point.x)
        
        seller_list.append({
            "seller": SellerSchema(
                id=seller.id,
                name=seller.name,
                contact=seller.contact,
                address=seller.address,
                coordinates=coordinates
            ),
            "distance_km": round(distance/1000, 2)  # Convert meters to km
        })
    return seller_list
 
@router.post("/products/add", response_model=Product)
async def add_product_api(name: str = Form(...),
            desc: str = Form(None),
            category: str = Form(None),
            images: List[UploadFile] = File(...),
            db: Session = Depends(get_db)):
    
    return await add_product(name,desc,category,images,db)

