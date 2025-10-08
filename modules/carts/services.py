from typing import Dict, Optional, List
from .schemas import CartItemCreate
from modules.products import services as product_services
from modules.promos import services as promo_services
from modules.transactions import services as transaction_services

# Keranjang belanja global (karena tidak ada user session)
cart_db: Dict[str, List[Dict]] = {"items": []}

def get_current_cart() -> Dict:
    total_price = 0
    detailed_items = []
    
    for item in cart_db["items"]:
        product = product_services.find_product_by_id(item["product_id"])
        if product:
            item_total = product["price"] * item["quantity"]
            total_price += item_total
            detailed_items.append({
                "product_id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "quantity": item["quantity"]
            })
            
    return {"items": detailed_items, "total_price": total_price}


def add_item_to_cart(item_data: CartItemCreate) -> Dict:
    product = product_services.find_product_by_id(item_data.product_id)
    if not product:
        raise ValueError("Product not found")
    
    if product["stock"] < item_data.quantity:
        raise ValueError("Insufficient stock")

    for existing_item in cart_db["items"]:
        if existing_item["product_id"] == item_data.product_id:
            new_quantity = existing_item["quantity"] + item_data.quantity
            if product["stock"] < new_quantity:
                raise ValueError("Insufficient stock for updated quantity")
            existing_item["quantity"] = new_quantity
            return get_current_cart()

    # UPDATED: Menggunakan .model_dump() sebagai pengganti .dict()
    cart_db["items"].append(item_data.model_dump())
    return get_current_cart()

def remove_item_from_cart(product_id: int) -> Optional[Dict]:
    item_to_remove = None
    for item in cart_db["items"]:
        if item["product_id"] == product_id:
            item_to_remove = item
            break
    
    if item_to_remove:
        cart_db["items"].remove(item_to_remove)
        return get_current_cart()
    
    return None

def process_checkout(promo_code: Optional[str] = None) -> Dict:
    cart_details = get_current_cart()
    if not cart_details["items"]:
        raise ValueError("Cart is empty")

    original_price = cart_details["total_price"]
    final_price = original_price
    discount_applied = 0.0
    
    for item in cart_details["items"]:
        product = product_services.find_product_by_id(item["product_id"])
        if not product or product["stock"] < item["quantity"]:
            raise ValueError(f"Insufficient stock for product: {item['name']}")

    if promo_code:
        promo = promo_services.find_promo_by_code(promo_code)
        if not promo:
            raise ValueError("Invalid promo code")
        
        discountable_amount = 0
        for item in cart_details["items"]:
            if item["product_id"] in promo["product_ids"]:
                discountable_amount += item["price"] * item["quantity"]
        
        discount_applied = discountable_amount * (promo["discount_percentage"] / 100)
        final_price = original_price - discount_applied

    for item in cart_details["items"]:
        product = product_services.find_product_by_id(item["product_id"])
        product["stock"] -= item["quantity"]

    transaction = transaction_services.create_transaction(
        items=cart_details["items"],
        total_price=final_price,
        promo_used=promo_code
    )
    
    cart_db["items"].clear()
    
    return {
        "transaction_id": transaction["id"],
        "original_price": original_price,
        "discount_applied": discount_applied,
        "final_price": final_price,
        "message": "Checkout successful!"
    }