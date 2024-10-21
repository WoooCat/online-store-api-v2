from typing import Optional

from pydantic import BaseModel


class PaginationParams(BaseModel):
    cursor: Optional[int] = None
    limit: int = 10

    class Config:
        json_schema_extra = {"example": {"cursor": 100, "limit": 10}}
