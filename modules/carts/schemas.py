from pydantic import BaseModel, Field
from typing import List, Optional

class CartItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)

class CartItemCreate(CartItemBase):
    pass

class CartItem(CartItemBase):
    name: str
    price: float
    
class Cart(BaseModel):
    items: List[CartItem]
    total_price: float = 0.0

class CheckoutInfo(BaseModel):
    transaction_id: int
    original_price: float
    discount_applied: float
    final_price: float
    message: str