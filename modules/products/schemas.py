from pydantic import BaseModel, Field, ConfigDict

class ProductBase(BaseModel):
   
    name: str = Field(..., min_length=3, max_length=50, json_schema_extra={'example': "Laptop Gaming"})
    price: float = Field(..., gt=0, json_schema_extra={'example': 15000000.0})
    stock: int = Field(..., ge=0, json_schema_extra={'example': 10})
    description: str = Field(..., json_schema_extra={'example': "Ini adalah deskripsi produk."})

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    
   
    model_config = ConfigDict(from_attributes=True)