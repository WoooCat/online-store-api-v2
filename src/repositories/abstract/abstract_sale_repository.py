from abc import ABC, abstractmethod

from src.infrastructure.db.models.models import Product, Sale


class AbstractSaleRepository(ABC):
    """
    Abstract repository for managing sale-related operations.

    This interface defines the core operations required for handling sales,
    such as purchasing a product. Implementations of this repository
    should interact with a specific data source (e.g., database).
    """

    @abstractmethod
    async def buy_product(self, product: Product, quantity: int) -> Sale:
        """Create a sale for a given product and quantity."""
        pass
