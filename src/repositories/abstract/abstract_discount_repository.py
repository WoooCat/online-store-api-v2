from abc import ABC, abstractmethod
from typing import List, Optional

from src.infrastructure.db.models.models import Discount


class AbstractDiscountRepository(ABC):
    """
    This abstract class defines the interface for interacting with the Discount data source.

    It enforces the implementation of key methods that handle the core operations for
    managing discounts in the system, including adding, retrieving, and deleting discounts.

    Subclasses should provide concrete implementations of these methods using the specific
    persistence mechanism (e.g., SQLAlchemy, in-memory storage, etc.).
    """

    @abstractmethod
    async def add_discount(self, discount: Discount) -> Discount:
        """Add new discount to the database."""
        pass

    @abstractmethod
    async def get_discount_by_id(self, discount_id: int) -> Optional[Discount]:
        """Retrieve a discount by its ID from DB."""
        pass

    @abstractmethod
    async def get_all_discounts(
        self, cursor: Optional[int], limit: int
    ) -> List[Discount]:
        """Retrieve all discounts with pagination from DB."""
        pass

    @abstractmethod
    async def delete_discount(self, discount_id: int) -> bool:
        """Delete a discount by its ID."""
        pass
