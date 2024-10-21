from typing import List

from fastapi import APIRouter, Depends, status

from src.dependencies.service_dependencies import get_category_service
from src.schemes.category_schemes import CategoryCreateRequest, CategoryResponse, CategoryUpdateRequest
from src.services.category_service import CategoryService

router = APIRouter(prefix="/category", tags=["category"])


@router.get("/categories/", response_model=List[CategoryResponse])
async def get_all_categories(
    category_service: CategoryService = Depends(get_category_service),
):
    """Retrieve all Categories."""
    categories = await category_service.get_all_categories()
    return categories


@router.post(
    "/categories/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED
)
async def add_category(
    category_data: CategoryCreateRequest,
    category_service: CategoryService = Depends(get_category_service),
):
    """Add new Category."""
    return await category_service.add_category(category_data.dict())


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category_by_id(
    category_id: int, category_service: CategoryService = Depends(get_category_service)
):
    """Retrieve a specific Category by its ID."""
    category = await category_service.get_category_by_id(category_id)
    return CategoryResponse.from_orm(category)


@router.get("/name/{name}", response_model=CategoryResponse)
async def get_category_by_name(
    name: str, category_service: CategoryService = Depends(get_category_service)
):
    """Retrieve all Categories."""
    category = await category_service.get_category_by_name(name)
    return category


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category_data: CategoryUpdateRequest,
    category_service: CategoryService = Depends(get_category_service),
):
    """Update a specific Category by its ID."""
    return await category_service.update_category_by_id(
        category_id, category_data.dict()
    )


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int, category_service: CategoryService = Depends(get_category_service)
):
    """Delete a specific Category by its ID."""
    await category_service.delete_category(category_id)
