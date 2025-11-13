"""
Database Schemas for Abbey Bites

Each Pydantic model represents a collection in MongoDB. The collection name
is the lowercase of the class name (e.g., MenuItem -> "menuitem").
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class MenuItem(BaseModel):
    name: str = Field(..., description="Dish name")
    description: Optional[str] = Field(None, description="Short description of the dish")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field("Main", description="Category like Starters, Mains, Drinks, Desserts")
    image: Optional[str] = Field(None, description="Image URL")
    is_available: bool = Field(True, description="Whether the dish is available")


class OrderItem(BaseModel):
    item_id: str = Field(..., description="Referenced menu item _id as string")
    name: str = Field(..., description="Snapshot name of the item when ordered")
    price: float = Field(..., ge=0, description="Snapshot price at order time")
    quantity: int = Field(..., ge=1, description="Quantity ordered")


class CustomerInfo(BaseModel):
    name: str
    phone: str
    address: str
    notes: Optional[str] = None


class Order(BaseModel):
    items: List[OrderItem]
    customer: CustomerInfo
    total: float = Field(..., ge=0)
    status: str = Field("pending", description="pending | confirmed | preparing | out_for_delivery | delivered | cancelled")
    payment_method: str = Field("COD", description="COD | Card | Online")
