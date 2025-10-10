from typing import List
from fastapi import APIRouter, HTTPException, status, Header
from typing import Optional
from . import schemas
from . import services

router = APIRouter()

@router.post("/", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
def create_product(
    product: schemas.ProductCreate, 
    x_user_role: Optional[str] = Header(None)
):
    """(Admin) Menambahkan produk baru."""

    if x_user_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Only admin can add products"
        )
    return services.create_new_product(product)

@router.get("/", response_model=List[schemas.Product])
def get_products():
    """(User & Admin) Menampilkan semua produk."""
    return services.get_all_products()

@router.get("/{product_id}", response_model=schemas.Product)
def get_product(product_id: int):
    """(User & Admin) Menampilkan detail satu produk."""
    product = services.find_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product_data: schemas.ProductCreate):
    """(Admin) Memperbarui data produk."""
    updated_product = services.update_existing_product(product_id, product_data)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.delete("/{product_id}", response_model=schemas.Product)
def delete_product(product_id: int):
    """(Admin) Menghapus produk."""
    deleted_product = services.delete_product_by_id(product_id)
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return deleted_product