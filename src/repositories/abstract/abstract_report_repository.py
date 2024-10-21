from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from src.infrastructure.db.models.models import Sale


class AbstractSaleRepository(ABC):
    """
    Abstract repository for fetching sales data.

    This interface defines a method to generate sales reports based on various filters,
    such as product details, category, and date range. Implementations of this repository
    should provide concrete logic for querying sales  from the data source (e.g., SQLAlchemy, in-memory storage, etc.).
    """

    @abstractmethod
    async def generate_sales_report(
        self,
        product_id: Optional[int] = None,
        product_name: Optional[str] = None,
        category_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Sale]:
        """Generate a sales report based on the provided filters."""
        pass
