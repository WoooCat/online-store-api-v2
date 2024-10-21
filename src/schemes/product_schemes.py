from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    """Base schema for Product."""

    name: str
    description: str
    price: float
    stock: Optional[int] = None

    class Config:
        from_attributes = True


class ProductCreateRequest(ProductBase):
    """Schema for creating a new Product."""

    category_id: int


class ProductPriceUpdateRequest(BaseModel):
    """Schema for updating the price of a Product."""

    price: float

    class Config:
        from_attributes = True


class ProductUpdateRequest(BaseModel):
    """Schema for updating an existing Product."""

    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    stock: Optional[int] = None

    class Config:
        from_attributes = True


class ProductResponse(BaseModel):
    """Schema for returning product information, including computed fields like final price and discount details."""

    id: int
    name: str
    description: str
    price: float
    final_price: float
    category_id: int
    category_name: str
    discount_id: Optional[int] = None
    discount_name: Optional[str] = None
    stock: Optional[int] = None
    reserved_quantity: Optional[int] = None

    class Config:
        from_attributes = True
