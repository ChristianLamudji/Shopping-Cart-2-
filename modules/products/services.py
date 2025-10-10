import csv
from typing import List, Dict, Optional
from .schemas import ProductCreate

products_db: List[Dict] = []
product_id_counter = 0

def load_products_from_csv():
    """Membaca data produk dari file CSV dan memuatnya ke dalam memori."""
    global product_id_counter
    try:
        with open('data/toserba_products_with_desc.csv', mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                product = {
                    "id": int(row["id"]),
                    "name": row["name"],
                    "price": float(row["price"]),
                    "stock": int(row["stock"]),
                    "description": row["description"]
                }
                products_db.append(product)
        
        if products_db:
            product_id_counter = max(p["id"] for p in products_db)
    except FileNotFoundError:
        print("PERINGATAN: File CSV tidak ditemukan. Memulai dengan daftar produk kosong.")
    except Exception as e:
        print(f"ERROR: Gagal memuat produk dari CSV: {e}")


load_products_from_csv()

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
    
    new_product = product_data.model_dump()
    new_product["id"] = product_id_counter
    products_db.append(new_product)
    return new_product

def update_existing_product(product_id: int, product_data: ProductCreate) -> Optional[Dict]:
    for product in products_db:
        if product["id"] == product_id:
            update_data = product_data.model_dump(exclude_unset=True)
            product.update(update_data)
            return product
    return None

def delete_product_by_id(product_id: int) -> bool:
    product_to_delete = find_product_by_id(product_id)
    if product_to_delete:
        products_db.remove(product_to_delete)
        return True
    return False