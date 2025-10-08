from typing import Optional
from fastapi import APIRouter, HTTPException, status, Query
from . import schemas
from . import services

router = APIRouter()

@router.post("/", response_model=schemas.Cart)
def add_to_cart(item: schemas.CartItemCreate):
    """(User) Menambahkan produk ke keranjang atau memperbarui kuantitas."""
    try:
        cart = services.add_item_to_cart(item)
        return cart
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=schemas.Cart)
def view_cart():
    """(User) Melihat isi keranjang belanja."""
    return services.get_current_cart()
    
@router.delete("/{product_id}", response_model=schemas.Cart)
def remove_from_cart(product_id: int):
    """(User) Menghapus produk dari keranjang."""
    updated_cart = services.remove_item_from_cart(product_id)
    if updated_cart is None:
        raise HTTPException(status_code=404, detail="Product not found in cart")
    return updated_cart

@router.post("/checkout", response_model=schemas.CheckoutInfo)
def checkout(promo_code: Optional[str] = Query(None, description="Kode promo yang ingin digunakan")):
    """(User) Proses checkout keranjang belanja."""
    try:
        result = services.process_checkout(promo_code)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))