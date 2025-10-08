from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_01_get_initial_products():
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 2

def test_02_add_item_to_cart():
    response = client.post("/cart/", json={"product_id": 1, "quantity": 1})
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == 1
    assert data["total_price"] == 20000000.0

def test_03_add_another_item_to_cart():
    response = client.post("/cart/", json={"product_id": 2, "quantity": 2})
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["total_price"] == 20500000.0

def test_04_add_item_insufficient_stock():
    response = client.post("/cart/", json={"product_id": 1, "quantity": 10})
    assert response.status_code == 400
    assert "Insufficient stock" in response.json()["detail"]

def test_05_checkout_with_valid_promo():
    response = client.post("/cart/checkout?promo_code=DISKON50")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Checkout successful!"
    assert data["original_price"] == 20500000.0
    assert data["discount_applied"] == 10000000.0
    assert data["final_price"] == 10500000.0

def test_06_cart_is_empty_after_checkout():
    response = client.get("/cart/")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 0
    assert data["total_price"] == 0.0

def test_07_check_stock_deduction():
    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json()["stock"] == 4
    
    response = client.get("/products/2")
    assert response.status_code == 200
    assert response.json()["stock"] == 48

def test_08_transaction_history_is_recorded():
    response = client.get("/transactions/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["total_price"] == 10500000.0
    assert data[0]["promo_used"] == "DISKON50"