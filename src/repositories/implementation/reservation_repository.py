from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.infrastructure.db.context_managers import transaction_context
from src.infrastructure.db.models.models import Reservation
from src.repositories.abstract.abstract_reservation_repository import AbstractReservationRepository


class ReservationRepository(AbstractReservationRepository):
    """
    SQLAlchemy implementation of the AbstractReservationRepository for managing reservations.

    This repository provides methods to handle reservation operations such as creating, canceling,
    and retrieving reservations, using SQLAlchemy for database interaction.
    """

    def __init__(self, db: AsyncSession):
        """
        Init repository with DB session.
        """
        self.db = db

    async def reserve_product(self, product_id: int, quantity: int) -> Reservation:
        """
        Create and persist a new reservation for the given product and quantity in DB.
        """
        async with transaction_context(self.db):
            reservation = Reservation(product_id=product_id, quantity=quantity)
            self.db.add(reservation)
            await self.db.commit()
            await self.db.refresh(reservation)
            return reservation

    async def cancel_reservation(self, reservation_id: int) -> bool:
        """Cancel an active reservation by marking it as inactive in DB."""
        async with transaction_context(self.db):
            reservation = await self.get_reservation_by_id(reservation_id)
            if reservation:
                reservation.active = False
                await self.db.commit()
                await self.db.refresh(reservation)
                return True
            return False

    async def get_reservation_by_id(self, reservation_id: int) -> Optional[Reservation]:
        """Retrieve a Reservation by its ID from DB."""
        query = select(Reservation).filter(Reservation.id == reservation_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_reservations_by_product_id(
        self, product_id: int, cursor: Optional[int], limit: int = 10,
    ) -> List[Reservation]:
        """Retrieve reservations for a specific product with pagination from DB."""
        query = select(Reservation).filter(Reservation.product_id == product_id)

        if cursor is not None:
            query = query.filter(Reservation.id > cursor)
        query = query.order_by(Reservation.id).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().fetchmany(limit)

    async def get_all_reservations(
        self, cursor: Optional[int], limit: int = 10
    ) -> List[Reservation]:
        """Retrieve all Reservations with pagination from DB"""
        query = select(Reservation)

        if cursor is not None:
            query = query.filter(Reservation.id > cursor)
        query = query.order_by(Reservation.id).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().fetchmany(limit)
