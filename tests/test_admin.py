from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Definisikan header admin untuk digunakan kembali
admin_headers = {"x-user-role": "admin"}

def test_create_product_as_user_fails():
    """Tes: Gagal membuat produk jika tanpa header admin (sebagai user)."""
    response = client.post(
        "/products",
        json={"name": "Forbidden Product", "price": 100, "stock": 10, "description": "This should fail"}
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Only admin can add products"

def test_create_product_as_admin_succeeds():
    """Tes: Berhasil membuat produk jika menggunakan header admin."""
    response = client.post(
        "/products",
        headers=admin_headers,
        json={
            "name": "Admin Product", 
            "price": 100, 
            "stock": 10, 
            "description": "A product added by an admin." # <-- DESKRIPSI DITAMBAHKAN
        }
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Admin Product"

def test_create_promo_as_user_fails():
    """Tes: Gagal membuat promo jika tanpa header admin (sebagai user)."""
    response = client.post(
        "/promos",
        json={"code": "FAILPROMO", "discount_percentage": 10, "product_ids": [1]}
    )
    assert response.status_code == 403
    # Perbaiki detail pesan error agar sesuai dengan kode
    assert response.json()["detail"] == "Admin access required"

def test_create_promo_as_admin_succeeds():
    """Tes: Berhasil membuat promo jika menggunakan header admin."""
    response = client.post(
        "/promos",
        headers=admin_headers,
        json={"code": "SUCCESSPROMO", "discount_percentage": 25, "product_ids": [1]}
    )
    assert response.status_code == 201
    assert response.json()["code"] == "SUCCESSPROMO"