from fastapi import FastAPI
from modules.products import routes as product_routes
from modules.carts import routes as cart_routes
from modules.promos import routes as promo_routes
from modules.transactions import routes as transaction_routes

app = FastAPI(
    title="E-commerce API",
    description="API untuk mengelola produk, keranjang belanja, dan promo.",
    version="1.0.0"
)

# Menggabungkan router dari setiap modul
app.include_router(product_routes.router, prefix="/products", tags=["📦 Products"])
app.include_router(cart_routes.router, prefix="/cart", tags=["🛒 Cart"])
app.include_router(promo_routes.router, prefix="/promos", tags=["💲 Promos"])
app.include_router(transaction_routes.router, prefix="/transactions", tags=["🧾 Transactions"])

@app.get("/", tags=["🏠 Home"])
def read_root():
    return {"message": "Welcome to the E-commerce API!"}