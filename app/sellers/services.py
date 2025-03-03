import os
from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, ForeignKey
from app.products.models import ProductModel
from geoalchemy2 import WKTElement
from .models import SellerModel, ProductSellerModel
from .schemas import ProductSeller, SellerResponse, Seller
from geoalchemy2.shape import from_shape, to_shape

def add_seller(seller, db):
    coordinates = WKTElement(f"POINT({seller.longitude} {seller.latitude})", srid=4326)

    
    seller_db = SellerModel(
        name=seller.name,
        contact=seller.contact,
        coordinates=coordinates,  # Convert lat/lon to PostGIS format
    )
    db.add(seller_db)
    db.commit()
    db.refresh(seller_db)  # Fetch the latest data from DB 
    return SellerResponse(id=seller_db.id, **seller.model_dump())


def add_product_seller(data, db):
    product_seller = ProductSellerModel(
        product_id=data.product_id,
        seller_id=data.seller_id,
        price=data.price
    )
    db.add(product_seller)
    db.commit()
    return {"message": "Product linked to seller successfully"}

def get_sellers(db):
    sellers = db.query(SellerModel).all()
    seller_responses = []
    for s in sellers:
        point = to_shape(s.coordinates)
        seller_responses.append(SellerResponse(id=s.id,
                                                name=s.name,
                                                contact=s.contact,
                                                latitude=point.x,  # Assuming location is a geometry(Point) field
                                                longitude=point.y))
    return seller_responses