from fastapi.testclient import TestClient
from main import app

client = TestClient(app)



def test_01_get_initial_products():
    """Tes untuk memastikan produk dari CSV berhasil dimuat."""
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 100

def test_02_add_item_to_cart():
    """Tes menambah item pertama (ID 1) ke keranjang."""
    response = client.post("/cart/", json={"product_id": 1, "quantity": 1})
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == 1
    assert data["total_price"] == 34000.0 

def test_03_add_another_item_to_cart():
    """Tes menambah item kedua (ID 2, sebanyak 2 buah) ke keranjang."""
    response = client.post("/cart/", json={"product_id": 2, "quantity": 2})
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
   
    assert data["total_price"] == 34000.0 + 242000.0

def test_04_add_item_insufficient_stock():
    """Tes validasi stok. Stok produk ID 2 adalah 20, kita coba beli 21."""
    response = client.post("/cart/", json={"product_id": 2, "quantity": 21})
    assert response.status_code == 400 
    assert "Insufficient stock" in response.json()["detail"]

def test_05_checkout_with_valid_promo():
    """Tes checkout dengan promo 'DISKON50'."""
    response = client.post("/cart/checkout?promo_code=DISKON50")
    assert response.status_code == 200
    data = response.json()
    
   
    original_price = 34000.0 + 242000.0  
    discount = 34000.0 * 0.5 
    final_price = original_price - discount
    

    assert data["message"] == "Checkout successful!"
    assert data["original_price"] == original_price
    assert data["discount_applied"] == discount
    assert data["final_price"] == final_price

def test_06_cart_is_empty_after_checkout():
    """Tes memastikan keranjang kosong setelah checkout."""
    response = client.get("/cart/")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 0
    assert data["total_price"] == 0.0

def test_07_check_stock_deduction():
    """Tes verifikasi stok berkurang setelah checkout."""
    
    response_1 = client.get("/products/1")
    assert response_1.status_code == 200
    assert response_1.json()["stock"] == 60

    
    response_2 = client.get("/products/2")
    assert response_2.status_code == 200
    assert response_2.json()["stock"] == 18

def test_08_transaction_history_is_recorded():
    """Tes verifikasi transaksi tercatat dengan benar."""
    response = client.get("/transactions/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    
    
    original_price = 34000.0 + 242000.0
    discount = 34000.0 * 0.5
    final_price_from_checkout = original_price - discount
    

    assert data[0]["total_price"] == final_price_from_checkout
    assert data[0]["promo_used"] == "DISKON50"