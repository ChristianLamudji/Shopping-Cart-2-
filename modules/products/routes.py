from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Header
from . import schemas, services

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
def update_product(
    product_id: int, 
    product_data: schemas.ProductCreate,
    x_user_role: Optional[str] = Header(None)
):
    """(Admin) Memperbarui data produk."""
    if x_user_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Admin access required"
        )
    updated_product = services.update_existing_product(product_id, product_data)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, x_user_role: Optional[str] = Header(None)):
    """(Admin) Menghapus produk."""
    if x_user_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Admin access required"
        )
    
    was_deleted = services.delete_product_by_id(product_id)
    if not was_deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return