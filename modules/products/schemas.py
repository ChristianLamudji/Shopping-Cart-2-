from pydantic import BaseModel, Field, ConfigDict

class ProductBase(BaseModel):
    # UPDATED: Menggunakan json_schema_extra untuk 'example'
    name: str = Field(..., min_length=3, max_length=50, json_schema_extra={'example': "Laptop Gaming"})
    price: float = Field(..., gt=0, json_schema_extra={'example': 15000000.0})
    stock: int = Field(..., ge=0, json_schema_extra={'example': 10})

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    
    # UPDATED: Menggunakan ConfigDict dan from_attributes
    model_config = ConfigDict(from_attributes=True)