from typing import List, Dict
import datetime

transactions_db: List[Dict] = []
transaction_id_counter = 0

def create_transaction(items: List[Dict], total_price: float, promo_used: str = None) -> Dict:
    global transaction_id_counter
    transaction_id_counter += 1
    
    new_transaction = {
        "id": transaction_id_counter,
        "timestamp": datetime.datetime.now().isoformat(),
        "items": items,
        "total_price": total_price,
        "promo_used": promo_used
    }
    transactions_db.append(new_transaction)
    return new_transaction

def get_all_transactions() -> List[Dict]:
    return transactions_db