import os
from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, ForeignKey
from app.products.models import ProductModel


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True) 

def get_products(db):
    return db.query(ProductModel).all()


async def add_product(name, desc, category, images, db):
    
    image_urls = []
    
    for image in images:
        file_location = os.path.join(UPLOAD_DIR, image.filename)
        with open(file_location, "wb") as buffer:
            buffer.write(await image.read())  # Save image file

        image_url = f"/static/{image.filename}"  # URL to access the image
        image_urls.append(image_url)

    new_product = ProductModel(
        name=name,
        desc=desc,
        category=category,
        images=image_urls
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product
