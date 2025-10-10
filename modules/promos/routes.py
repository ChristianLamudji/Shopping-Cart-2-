from typing import List, Optional
from fastapi import APIRouter, Header, HTTPException
from . import services, schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.Promo])
def get_all_promos_route():
    """(User & Admin) Melihat daftar semua kode promo yang tersedia."""
    return services.get_all_promos()

@router.post("/", response_model=schemas.Promo, status_code=201)
def create_promo(promo: schemas.PromoCreate, x_user_role: Optional[str] = Header(None)):
    """(Admin) Membuat kode promo baru."""
    if x_user_role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
        
    new_promo = services.create_new_promo(promo)
    if not new_promo:
        raise HTTPException(status_code=400, detail="Promo code already exists")
    return new_promo

@router.get("/", response_model=List[schemas.Promo])
def get_promos():
    """(Admin) Menampilkan semua kode promo yang aktif."""
    return services.get_all_promos()