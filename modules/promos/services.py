from typing import Optional
from .schemas import PromoCreate

promos_db = {
    "DISKON50": {"code": "DISKON50", "discount_percentage": 50.0, "product_ids": [1]}
}

def find_promo_by_code(code: str) -> Optional[dict]:
    """Mencari promo berdasarkan kodenya."""
    return promos_db.get(code)

def create_new_promo(promo: PromoCreate) -> Optional[dict]:
    """Membuat promo baru dan menyimpannya di memori."""
    if promo.code in promos_db:
        return None
    new_promo_dict = promo.model_dump()
    promos_db[promo.code] = new_promo_dict
    return new_promo_dict

def get_all_promos() -> list:
    """Mengembalikan daftar semua promo yang tersimpan."""
    return list(promos_db.values())