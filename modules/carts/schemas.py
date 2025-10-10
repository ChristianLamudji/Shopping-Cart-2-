from typing import List, Optional
from pydantic import BaseModel, Field

class CartItemBase(BaseModel):
    product_id: int
    quantity: int

class CartItemCreate(CartItemBase):
    pass

class CartItem(BaseModel):
    product_id: int
    name: str
    quantity: int
    price: float
    description: str

class Cart(BaseModel):
    items: List[CartItem]
    total_price: float

class CheckoutInfo(BaseModel):
    message: str
    original_price: float
    discount_applied: float
    final_price: float
    transaction_details: dict

class CartItemUpdate(BaseModel):
    """Skema untuk mengubah kuantitas item di keranjang."""
    quantity: int = Field(..., ge=1, description="Jumlah baru harus minimal 1")