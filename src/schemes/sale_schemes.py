from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SaleBase(BaseModel):
    """Base schema for Sale, defining common fields such as product ID, quantity, discount ID, and the sale date."""

    product_id: int
    quantity: int
    discount_id: Optional[int] = None
    sold_at: datetime = datetime.utcnow()

    class Config:
        from_attributes = True


class SaleRequest(BaseModel):
    """
    Schema for requesting a product sale, containing product ID and quantity.
    """

    product_id: int
    quantity: int


class SaleFilterRequest(BaseModel):
    """
    Schema for filtering sales data based on various criteria, such as product ID, name, category, or date range.
    """

    product_id: Optional[int] = None
    product_name: Optional[str] = None
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class SaleResponse(BaseModel):
    """
    Schema for the sale response, including detailed product, discount, and category information,
    along with the sale quantity and sale date.
    """

    id: int
    product_id: int
    product_name: str
    product_price: float
    discount_name: Optional[str]
    category_id: Optional[int]
    category_name: Optional[str]
    quantity: int
    sold_at: datetime

    class Config:
        from_attributes = True
