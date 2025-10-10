from typing import Optional
from fastapi import APIRouter, HTTPException
from . import services, schemas

router = APIRouter()

@router.post("/", response_model=schemas.Cart)
def add_to_cart(item: schemas.CartItemCreate):
    try:
        cart = services.add_item_to_cart(item.product_id, item.quantity)
        return cart
    except HTTPException as e:
        raise e

@router.get("/", response_model=schemas.Cart)
def view_cart():
    return services.get_current_cart()

@router.put("/{product_id}", response_model=schemas.Cart)
def update_cart_item_quantity(product_id: int, item: schemas.CartItemUpdate):
    """Mengubah jumlah produk tertentu di dalam keranjang."""
    try:
        updated_cart = services.update_item_quantity(product_id, item.quantity)
        if updated_cart is None:
            raise HTTPException(status_code=404, detail="Product not found in cart")
        return updated_cart
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{product_id}", response_model=schemas.Cart)
def remove_from_cart(product_id: int):
    updated_cart = services.remove_item_from_cart(product_id)
    if updated_cart is None:
        raise HTTPException(status_code=404, detail="Product not found in cart")
    return updated_cart

@router.post("/checkout", response_model=schemas.CheckoutInfo)
def checkout(promo_code: Optional[str] = None):
    try:
        result = services.process_checkout(promo_code)
        return result
    except HTTPException as e:
        raise e