from datetime import datetime

from pydantic import BaseModel


class ReservationBase(BaseModel):
    product_id: int
    quantity: int
    reserved_at: datetime = datetime.utcnow()
    active: bool = True

    class Config:
        from_attributes = True


class ReservationCreateRequest(ReservationBase):
    pass


class ReservationRequest(BaseModel):
    product_id: int
    quantity: int


class ReservationResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    active: bool

    class Config:
        from_attributes = True
