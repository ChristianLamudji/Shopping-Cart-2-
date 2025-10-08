from typing import List
from fastapi import APIRouter
from . import services

router = APIRouter()

@router.get("/", response_model=List[dict])
def get_transaction_history():
    """(Admin) Melihat riwayat semua transaksi."""
    return services.get_all_transactions()