from fastapi import APIRouter, HTTPException, status, Header
from typing import Optional, List
from . import schemas
from . import services

router = APIRouter()

@router.post("/", response_model=schemas.Promo, status_code=status.HTTP_201_CREATED)
def create_promo(
    promo: schemas.PromoCreate,
    x_user_role: Optional[str] = Header(None) # Tambahkan parameter header
):
    """(Admin) Membuat kode promo baru."""
    # Tambahkan blok pengecekan ini
    if x_user_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can add promos"
        )
    
    new_promo = services.create_new_promo(promo)
    if not new_promo:
        raise HTTPException(status_code=400, detail="Promo code already exists")
    return new_promo

@router.get("/", response_model=List[schemas.Promo])
def get_promos():
    """(Admin) Menampilkan semua kode promo yang aktif."""
    return services.get_all_promos()