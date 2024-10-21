from typing import List

from fastapi import APIRouter, Depends, status

from src.dependencies.service_dependencies import get_product_service
from src.schemes.pagination_schemes import PaginationParams
from src.schemes.product_schemes import (
    ProductCreateRequest,
    ProductPriceUpdateRequest,
    ProductResponse,
    ProductUpdateRequest,
)
from src.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[ProductResponse])
async def get_all_products(
    pagination: PaginationParams = Depends(),
    product_service: ProductService = Depends(get_product_service),
) -> List[ProductResponse]:
    """Retrieve all products with pagination."""
    return await product_service.get_all_products(
        cursor=pagination.cursor, limit=pagination.limit
    )


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def add_product(
    product_data: ProductCreateRequest,
    product_service: ProductService = Depends(get_product_service),
) -> ProductResponse:
    """Add new product."""
    return await product_service.add_product(product_data)


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product_by_id(
    product_id: int, product_service: ProductService = Depends(get_product_service),
) -> ProductResponse:
    """Retrieve a specific product by its ID."""
    return await product_service.get_product_by_id(product_id)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdateRequest,
    product_service: ProductService = Depends(get_product_service),
):
    """Update a specific product by its ID."""
    return await product_service.update_product(product_id, product_data.dict())


@router.patch("/{product_id}/price", response_model=ProductResponse)
async def update_price(
    product_id: int,
    price_data: ProductPriceUpdateRequest,
    product_service: ProductService = Depends(get_product_service),
):
    """Update the price of a product by its ID."""
    return await product_service.update_price(product_id, price_data.price)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int, product_service: ProductService = Depends(get_product_service)
):
    """Delete a specific product by its ID."""
    return await product_service.delete_product(product_id)


@router.get("/category/{category_id}", response_model=List[ProductResponse])
async def get_products_by_category(
    category_id: int,
    pagination: PaginationParams = Depends(),
    product_service: ProductService = Depends(get_product_service),
):
    """Retrieve products by category ID with pagination."""
    return await product_service.get_products_by_category(
        category_id, cursor=pagination.cursor, limit=pagination.limit
    )


@router.post("/products/{product_id}/discount", response_model=ProductResponse)
async def add_discount_to_product(
    product_id: int,
    discount_id: int,
    product_service: ProductService = Depends(get_product_service),
):
    """Add a discount to a product."""
    return await product_service.add_discount_to_product(product_id, discount_id)


@router.delete("/products/{product_id}/discount", response_model=ProductResponse)
async def remove_discount_from_product(
    product_id: int, product_service: ProductService = Depends(get_product_service)
):
    """Remove a discount from a product."""
    return await product_service.remove_discount_from_product(product_id)
