from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.infrastructure.db.context_managers import transaction_context
from src.infrastructure.db.models.models import Discount
from src.repositories.abstract.abstract_discount_repository import AbstractDiscountRepository


class DiscountRepository(AbstractDiscountRepository):
    """
    Concrete implementation of the AbstractDiscountRepository using SQLAlchemy for data persistence.

    This class provides the functionality to interact with the discount-related data stored in the database.
    It supports operations such as adding new discounts, retrieving discounts by their ID,
    fetching all discounts with pagination, and deleting discounts.

    The SQLAlchemy session is used for database transactions, ensuring that all changes are
    committed to the database and necessary data is refreshed after modification.
    """

    def __init__(self, db: AsyncSession):
        """Init DB session."""
        self.db = db

    async def add_discount(self, discount: Discount) -> Discount:
        """Add a new Discount to DB."""
        async with transaction_context(self.db):
            self.db.add(discount)
            await self.db.commit()
            await self.db.refresh(discount)
        return discount

    async def get_discount_by_id(self, discount_id: int) -> Optional[Discount]:
        """Retrieve a Discount by its ID form DB."""
        query = select(Discount).filter(Discount.id == discount_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all_discounts(
        self, cursor: Optional[int], limit: int = 10
    ) -> List[Discount]:
        """Retrieve all Discounts, with pagination from DB."""
        query = select(Discount)
        if cursor is not None:
            query = query.filter(Discount.id > cursor)
        query = query.order_by(Discount.id).limit(limit)
        result = await self.db.execute(query)

        return result.scalars().fetchmany(limit)

    async def delete_discount(self, discount_id: int) -> bool:
        """Delete a Discount by its ID from DB."""
        async with transaction_context(self.db):
            discount = await self.get_discount_by_id(discount_id)
            if discount:
                await self.db.delete(discount)
                await self.db.commit()
                return True
            return False
