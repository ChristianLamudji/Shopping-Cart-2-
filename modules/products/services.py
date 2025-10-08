from typing import List, Dict, Optional
from .schemas import ProductCreate

# Pengganti database (data disimpan selama server berjalan)
products_db: List[Dict] = [
    {"id": 1, "name": "Laptop Pro", "price": 20000000.0, "stock": 5},
    {"id": 2, "name": "Mouse Wireless", "price": 250000.0, "stock": 50},
]
product_id_counter = len(products_db)

def get_all_products() -> List[Dict]:
    return products_db

def find_product_by_id(product_id: int) -> Optional[Dict]:
    for product in products_db:
        if product["id"] == product_id:
            return product
    return None

def create_new_product(product_data: ProductCreate) -> Dict:
    global product_id_counter
    product_id_counter += 1
    new_product = {
        "id": product_id_counter,
        "name": product_data.name,
        "price": product_data.price,
        "stock": product_data.stock,
    }
    products_db.append(new_product)
    return new_product

def update_existing_product(product_id: int, product_data: ProductCreate) -> Optional[Dict]:
    product = find_product_by_id(product_id)
    if product:
        product["name"] = product_data.name
        product["price"] = product_data.price
        product["stock"] = product_data.stock
        return product
    return None

def delete_product_by_id(product_id: int) -> Optional[Dict]:
    product = find_product_by_id(product_id)
    if product:
        products_db.remove(product)
        return product
    return None