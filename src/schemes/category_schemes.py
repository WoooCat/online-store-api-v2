from typing import List, Optional

from pydantic import BaseModel

"""CATEGORY SCHEMES"""


class CategoryBase(BaseModel):
    """Base schema for Category containing shared fields."""

    name: str

    class Config:
        from_attributes = True


class CategoryCreateRequest(CategoryBase):
    """Schema for creating a new category."""

    parent_id: Optional[int] = None


class CategoryUpdateRequest(CategoryBase):
    """Schema for updating an existing category."""

    name: Optional[str] = None


class CategoryResponse(CategoryBase):
    """Schema for returning category information, including subcategories."""

    id: int
    parent_id: Optional[int] = None
    subcategories: Optional[List["CategoryResponse"]] = []
