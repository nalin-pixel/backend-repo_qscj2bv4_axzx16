"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional

# Grain business schemas

class GrainProduct(BaseModel):
    """
    Grain products available for sale
    Collection name: "grainproduct"
    """
    name: str = Field(..., description="Product name, e.g., Wheat")
    variety: Optional[str] = Field(None, description="Variety, e.g., Hard Red Winter")
    grade: Optional[str] = Field(None, description="Quality grade, e.g., Grade 1")
    price_per_ton: float = Field(..., ge=0, description="Price per metric ton in USD")
    stock_tons: float = Field(..., ge=0, description="Available stock in metric tons")
    origin: Optional[str] = Field(None, description="Country/Region of origin")
    moisture: Optional[float] = Field(None, ge=0, le=100, description="Moisture percentage")
    protein: Optional[float] = Field(None, ge=0, le=100, description="Protein percentage")
    description: Optional[str] = Field(None, description="Short description")
    image_url: Optional[HttpUrl] = Field(None, description="Image URL")

class Inquiry(BaseModel):
    """
    Buyer inquiries / RFQs
    Collection name: "inquiry"
    """
    name: str = Field(..., description="Contact name")
    email: str = Field(..., description="Contact email")
    phone: Optional[str] = Field(None, description="Phone number")
    product_name: Optional[str] = Field(None, description="Requested product name")
    product_id: Optional[str] = Field(None, description="Linked product id if known")
    quantity_tons: Optional[float] = Field(None, ge=0, description="Requested quantity in tons")
    message: Optional[str] = Field(None, description="Additional details")
    status: str = Field("new", description="Status of inquiry: new, contacted, closed")

# Example schemas kept for reference
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
