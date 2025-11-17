"""
Database Schemas for Flames Marketing Agency

Each Pydantic model maps to a MongoDB collection using the lowercase
class name as the collection name (e.g., Lead -> "lead").
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class Lead(BaseModel):
    """Inbound leads captured from the website forms"""
    name: str = Field(..., min_length=2, description="Full name")
    email: EmailStr
    phone: Optional[str] = Field(None, description="Phone number")
    service: Optional[str] = Field(None, description="Requested service id or name")
    message: Optional[str] = Field(None, description="Additional details from the prospect")
    source: str = Field("website", description="Acquisition source")


# Keep example schemas so DB viewer remains functional
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = None
    is_active: bool = True


class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True
