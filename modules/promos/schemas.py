from typing import List
from pydantic import BaseModel, Field, ConfigDict

class PromoBase(BaseModel):
    # UPDATED: Menggunakan json_schema_extra untuk 'example'
    code: str = Field(..., json_schema_extra={'example': "HEMAT10"})
    discount_percentage: float = Field(..., gt=0, le=100, json_schema_extra={'example': 10.0})
    product_ids: List[int] = Field(..., json_schema_extra={'example': [1, 2]})

class PromoCreate(PromoBase):
    pass

class Promo(PromoBase):
    # UPDATED: Menggunakan ConfigDict dan from_attributes
    model_config = ConfigDict(from_attributes=True)