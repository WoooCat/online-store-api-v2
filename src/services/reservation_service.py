from typing import List, Optional

from src.exceptions.exceptions import NotEnoughStockError, ProductNotFoundError, ReservationNotFoundError
from src.infrastructure.db.models.models import Reservation
from src.repositories.abstract.abstract_product_repository import AbstractProductRepository
from src.repositories.abstract.abstract_reservation_repository import AbstractReservationRepository


class ReservationService:
    """
    Service class for managing reservation-related business logic.

    This service is responsible for handling the core operations of reserving products,
    canceling reservations, and fetching reservation data. It coordinates with the product repository
    to ensure stock availability and adjusts stock levels when reservations are created or canceled.
    """

    def __init__(
        self,
        order_repo: AbstractReservationRepository,
        product_repo: AbstractProductRepository,
    ):
        """
        Initialize the ReservationService with the necessary repositories.

        :param order_repo: Repository for managing reservations.
        :param product_repo: Repository for managing products and stock.
        """
        self.order_repo = order_repo
        self.product_repo = product_repo

    async def reserve_product(self, product_id: int, quantity: int) -> Reservation:
        """Reserve a Product by reducing the stock and creating a reservation record."""
        product = await self.product_repo.get_product_by_id(product_id)
        if not product:
            raise ProductNotFoundError(product_id=product_id)
        if product.stock < quantity:
            raise NotEnoughStockError(product_id=product_id)

        reservation = await self.order_repo.reserve_product(
            product_id=product_id, quantity=quantity
        )

        if reservation:
            reservation_quantity = product.stock - quantity
            await self.product_repo.update_product_stock(
                product_id, reservation_quantity
            )

        return reservation

    async def cancel_reservation(self, reservation_id: int) -> None:
        """Cancel a reservation and restore the product's stock."""
        reservation = await self.order_repo.get_reservation_by_id(reservation_id)
        if not reservation or not reservation.active:
            raise ReservationNotFoundError(reservation_id=reservation_id)

        product = await self.product_repo.get_product_by_id(reservation.product_id)
        if not product:
            raise ProductNotFoundError(product_id=reservation.product_id)

        updated_stock = product.stock + reservation.quantity
        await self.order_repo.cancel_reservation(reservation_id)
        await self.product_repo.update_product_stock(product.id, updated_stock)

    async def get_all_reservations(
        self, cursor: Optional[int], limit: int
    ) -> List[Reservation]:
        """Retrieve all reservations with pagination."""
        return await self.order_repo.get_all_reservations(cursor=cursor, limit=limit)

    async def get_reservation_by_id(self, reservation_id: int) -> Optional[Reservation]:
        reservation = await self.order_repo.get_reservation_by_id(reservation_id)
        if not reservation:
            raise ReservationNotFoundError(reservation_id=reservation_id)
        return reservation

    async def get_reservations_by_product_id(
        self, product_id: int, cursor: Optional[int], limit: int,
    ) -> List[Reservation]:
        """Retrieve a Reservation by its ID."""
        reservations = await self.order_repo.get_reservations_by_product_id(
            product_id, cursor=cursor, limit=limit
        )
        product = await self.product_repo.get_product_by_id(product_id)
        if not product:
            raise ProductNotFoundError(product_id=product_id)
        if not reservations:
            raise ProductNotFoundError()
        return reservations
