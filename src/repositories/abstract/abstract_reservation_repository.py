from abc import ABC, abstractmethod
from typing import List, Optional

from src.infrastructure.db.models.models import Reservation


class AbstractReservationRepository(ABC):
    """
    This abstract class defines the interface for Reservation data management.

    This interface defines methods for core reservation operations, including:
    - Reserving a product
    - Fetching reservations by ID or product
    - Canceling reservations
    - Fetching all reservations with pagination support

    Subclasses should provide concrete implementations of these methods using the specific
    persistence mechanism (e.g., SQLAlchemy, in-memory storage, etc.).
    """

    @abstractmethod
    async def get_all_reservations(
        self, cursor: Optional[int], limit: int
    ) -> List[Reservation]:
        """
        Retrieve all reservations with pagination.
        """
        pass

    @abstractmethod
    async def reserve_product(self, product_id: int, quantity: int) -> Reservation:
        """
        Create a reservation for a product with the specified quantity.
        """
        pass

    @abstractmethod
    async def get_reservation_by_id(self, reservation_id: int) -> Optional[Reservation]:
        """
        Fetch a reservation by its ID.
        """
        pass

    @abstractmethod
    async def get_reservations_by_product_id(
        self, product_id: int, cursor: Optional[int], limit: int,
    ) -> List[Reservation]:
        """
        Retrieve all reservations for a specific product with pagination.
        """
        pass

    @abstractmethod
    async def cancel_reservation(self, reservation_id: int) -> bool:
        """
        Cancel a reservation and update its status.
        """
        pass
