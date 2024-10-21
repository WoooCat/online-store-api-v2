from abc import ABC, abstractmethod
from typing import List, Optional

from src.infrastructure.db.models.models import Product


class AbstractProductRepository(ABC):
    """Abstract base class for Product repository."""

    @abstractmethod
    async def get_all_products(
        self, cursor: Optional[int], limit: int
    ) -> List[Product]:
        """Retrieve all products with pagination."""
        pass

    @abstractmethod
    async def add_product(self, product_data: dict) -> Product:
        """Add a new product to the database."""
        pass

    @abstractmethod
    async def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Retrieve a product by its ID."""
        pass

    @abstractmethod
    async def update_product(self, product_id: int, updated_data: dict) -> Product:
        """Update a product by its ID."""
        pass

    @abstractmethod
    async def update_price(self, product_id: int, new_price: float) -> Product:
        """Update the price of a product by its ID."""
        pass

    @abstractmethod
    async def delete_product(self, product_id: int) -> bool:
        """Delete a product by its ID."""
        pass

    @abstractmethod
    async def get_products_by_category(
        self, category_id: int, cursor: Optional[int], limit: int
    ) -> List[Product]:
        """Retrieve products by category ID with pagination."""
        pass

    @abstractmethod
    async def add_discount_to_product(
        self, product_id: int, discount_id: int
    ) -> Product:
        """Add a discount to a product."""
        pass

    @abstractmethod
    async def remove_discount_from_product(self, product_id: int) -> Product:
        """Remove a discount from a product."""
        pass

    @abstractmethod
    def update_product_stock(self, product_id: int, param: dict) -> Product:
        """Update the stock of a product."""
        pass
