from typing import List, Dict, Optional
from fastapi import HTTPException
from modules.products import services as product_services
from modules.promos import services as promo_services
from modules.transactions import services as transaction_services

cart_db: Dict[int, int] = {}

def get_current_cart() -> Dict:
    items_in_cart = []
    total_price = 0.0

    for product_id, quantity in cart_db.items():
        product_info = product_services.find_product_by_id(product_id)
        if product_info:
            cart_item = {
                "product_id": product_id,
                "name": product_info["name"],
                "quantity": quantity,
                "price": product_info["price"],
                "description": product_info["description"] # <-- DIUBAH
            }
            items_in_cart.append(cart_item)
            total_price += product_info["price"] * quantity

    return {"items": items_in_cart, "total_price": total_price}

def add_item_to_cart(product_id: int, quantity: int) -> Dict:
    product_info = product_services.find_product_by_id(product_id)
    if not product_info:
        raise HTTPException(status_code=404, detail="Product not found")

    current_quantity_in_cart = cart_db.get(product_id, 0)
    if product_info["stock"] < current_quantity_in_cart + quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    cart_db[product_id] = current_quantity_in_cart + quantity
    return get_current_cart()

# KODE BARU UNTUK UPDATE KUANTITAS
def update_item_quantity(product_id: int, new_quantity: int) -> Optional[Dict]:
    """Mengubah kuantitas produk yang ada di keranjang."""
    if product_id not in cart_db:
        return None

    product_info = product_services.find_product_by_id(product_id)
    if not product_info or product_info["stock"] < new_quantity:
        raise ValueError("Insufficient stock for the new quantity")

    cart_db[product_id] = new_quantity
    return get_current_cart()

def remove_item_from_cart(product_id: int) -> Optional[Dict]:
    if product_id in cart_db:
        del cart_db[product_id]
        return get_current_cart()
    return None

def process_checkout(promo_code: Optional[str] = None) -> Dict:
    if not cart_db:
        raise HTTPException(status_code=400, detail="Cart is empty")

    cart_details = get_current_cart()
    original_price = cart_details["total_price"]
    final_price = original_price
    discount_applied = 0.0

    # Validasi stok sebelum checkout
    for item in cart_details["items"]:
        product_info = product_services.find_product_by_id(item["product_id"])
        if not product_info or product_info["stock"] < item["quantity"]:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product: {item['name']}")

    # Proses promo
    if promo_code:
        promo_info = promo_services.find_promo_by_code(promo_code)
        if not promo_info:
            raise HTTPException(status_code=404, detail="Promo code not found")
        
        applicable_items_price = sum(
            item["price"] * item["quantity"] 
            for item in cart_details["items"] 
            if item["product_id"] in promo_info["product_ids"]
        )
        
        discount_applied = applicable_items_price * (promo_info["discount_percentage"] / 100)
        final_price -= discount_applied

    # Kurangi stok
    for item in cart_details["items"]:
        product_info = product_services.find_product_by_id(item["product_id"])
        if product_info:
            product_info["stock"] -= item["quantity"]

    # Buat transaksi
    transaction = transaction_services.create_transaction(
        items=cart_details["items"],
        total_price=final_price,
        promo_used=promo_code
    )
    
    cart_db.clear()

    return {
        "message": "Checkout successful!",
        "original_price": original_price,
        "discount_applied": discount_applied,
        "final_price": final_price,
        "transaction_details": transaction
    }