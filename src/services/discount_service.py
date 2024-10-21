from typing import List, Optional

from src.exceptions.exceptions import DiscountNotFoundError
from src.infrastructure.db.models.models import Discount
from src.repositories.abstract.abstract_discount_repository import AbstractDiscountRepository


class DiscountService:
    """
    Service layer responsible for implementing business logic related to Discounts.

    This class acts as an intermediary between the API layer and the data access layer (repository).
    It handles the validation, processing, and orchestration of operations related to Discounts,
    such as creating new discounts, retrieving discount information by ID, fetching a paginated list of discounts,
    and deleting discounts.
    """

    def __init__(self, discount_repo: AbstractDiscountRepository):
        """Initialize the service with a Discount repository."""
        self.discount_repo = discount_repo

    async def add_discount(self, discount_data: dict) -> Discount:
        """Add a new Discount."""
        new_discount = Discount(**discount_data)
        return await self.discount_repo.add_discount(new_discount)

    async def get_discount_by_id(self, discount_id: int) -> Discount:
        """Retrieve a Discount by its ID. Raise DiscountNotFoundError if not found."""
        discount = await self.discount_repo.get_discount_by_id(discount_id)
        if not discount:
            raise DiscountNotFoundError(discount_id=discount_id)
        return discount

    async def get_all_discounts(
        self, cursor: Optional[int], limit: int
    ) -> List[Discount]:
        """Retrieve all discounts with pagination."""
        return await self.discount_repo.get_all_discounts(cursor=cursor, limit=limit)

    async def delete_discount(self, discount_id: int) -> None:
        """Delete a discount by its ID. Raise DiscountNotFoundError if not found."""
        success = await self.discount_repo.delete_discount(discount_id)
        if not success:
            raise DiscountNotFoundError(discount_id=discount_id)
