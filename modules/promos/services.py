from typing import Dict, Optional
from .schemas import PromoCreate

# Menggunakan dictionary agar pencarian kode promo lebih cepat
promos_db: Dict[str, Dict] = {
    "DISKON50": {
        "code": "DISKON50",
        "discount_percentage": 50.0,
        "product_ids": [1] # Hanya berlaku untuk produk dengan ID 1
    }
}

def find_promo_by_code(code: str) -> Optional[Dict]:
    return promos_db.get(code)

def create_new_promo(promo_data: PromoCreate) -> Optional[Dict]:
    if promo_data.code in promos_db:
        return None  # Kode promo sudah ada
    
    # UPDATED: Menggunakan .model_dump() sebagai pengganti .dict()
    new_promo = promo_data.model_dump()
    promos_db[promo_data.code] = new_promo
    return new_promo