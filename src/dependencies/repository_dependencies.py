from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.database import get_db
from src.repositories.implementation.category_repository import CategoryRepository
from src.repositories.implementation.discount_repository import DiscountRepository
from src.repositories.implementation.product_repository import ProductRepository
from src.repositories.implementation.report_repository import ReportRepository
from src.repositories.implementation.reservation_repository import ReservationRepository
from src.repositories.implementation.sale_repository import SaleRepository


def get_category_repository(db: AsyncSession = Depends(get_db)) -> CategoryRepository:
    """
    Returns a CategoryRepository instance, injecting the database session dependency.

    :param db: AsyncSession, the current database session.
    :return: An instance of CategoryRepository.
    """
    return CategoryRepository(db)


def get_product_repository(db: AsyncSession = Depends(get_db)) -> ProductRepository:
    """
    Returns a ProductRepository instance, injecting the database session dependency.

    :param db: AsyncSession, the current database session.
    :return: An instance of ProductRepository.
    """
    return ProductRepository(db)


def get_discount_repository(db: AsyncSession = Depends(get_db)) -> DiscountRepository:
    """
    Returns a DiscountRepository instance, injecting the database session dependency.

    :param db: AsyncSession, the current database session.
    :return: An instance of DiscountRepository.
    """
    return DiscountRepository(db)


def get_reservation_repository(
    db: AsyncSession = Depends(get_db),
) -> ReservationRepository:
    """
    Returns a ReservationRepository instance, injecting the database session dependency.

    :param db: AsyncSession, the current database session.
    :return: An instance of ReservationRepository.
    """
    return ReservationRepository(db)


def get_sale_repository(db: AsyncSession = Depends(get_db)) -> SaleRepository:
    """
    Returns a SaleRepository instance, injecting the database session dependency.

    :param db: AsyncSession, the current database session.
    :return: An instance of SaleRepository.
    """
    return SaleRepository(db)


def get_report_repository(db: AsyncSession = Depends(get_db)) -> ReportRepository:
    """
    Returns a ReportRepository instance, injecting the database session dependency.

    :param db: AsyncSession, the current database session.
    :return: An instance of ReportRepository.
    """
    return ReportRepository(db)
