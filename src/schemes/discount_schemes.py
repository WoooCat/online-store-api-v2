from pydantic import BaseModel


class DiscountCreateRequest(BaseModel):
    """Schema for creating a new Discount."""

    name: str
    percentage: float
    description: str = None


class DiscountResponse(BaseModel):
    """Schema for responding with Discount information."""

    id: int
    name: str
    percentage: float
    description: str = None

    class Config:
        from_attributes = True
