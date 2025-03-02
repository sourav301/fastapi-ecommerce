from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

class Product(BaseModel):
    id: int = 0
    name: str
    desc: Optional[str] = None  # Optional field with a default value
    created_at: Optional[datetime] = None
    category: Optional[str] = None
    images: List[str]
    class Config:
        from_attributes = True 