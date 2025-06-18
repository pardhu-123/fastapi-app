from pydantic import BaseModel

class ProductBase(BaseModel):
    Product: str
    HSN_CODE: str
    MRP: float

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    
    class Config:
        orm_mode = True