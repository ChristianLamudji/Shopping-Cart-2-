from fastapi import APIRouter, HTTPException, status
from . import schemas
from . import services

router = APIRouter()

@router.post("/", response_model=schemas.Promo, status_code=status.HTTP_201_CREATED)
def create_promo(promo: schemas.PromoCreate):
    """(Admin) Membuat kode promo baru."""
    new_promo = services.create_new_promo(promo)
    if not new_promo:
        raise HTTPException(status_code=400, detail="Promo code already exists")
    return new_promo