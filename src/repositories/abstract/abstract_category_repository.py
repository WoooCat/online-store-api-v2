from abc import ABC, abstractmethod
from typing import List, Optional

from src.infrastructure.db.models.models import Category


class AbstractCategoryRepository(ABC):
    """Abstract base class for Category repository."""

    @abstractmethod
    async def get_all_categories(self) -> List[Category]:
        """Retrieve all categories."""
        pass

    @abstractmethod
    async def add_category(self, category: Category) -> Category:
        """Add a new category."""
        pass

    @abstractmethod
    async def get_category_by_id(self, category_id: int) -> Optional[Category]:
        """Retrieve a category by its ID."""
        pass

    @abstractmethod
    async def get_category_by_name(self, name: str) -> Optional[Category]:
        """Retrieve a category by its name."""
        pass

    @abstractmethod
    async def update_category_by_id(
        self, category_id: int, updated_data: dict
    ) -> Optional[Category]:
        """Update a category by its ID with the given data."""
        pass

    @abstractmethod
    async def delete_category_by_id(self, category_id: int) -> bool:
        """Delete a category by its ID."""
        pass
