from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.database import get_db
from src.repositories.implementation.category_repository import CategoryRepository


def get_category_repository(db: AsyncSession = Depends(get_db)) -> CategoryRepository:
    """
    Returns a CategoryRepository instance, injecting the database session dependency.

    :param db: AsyncSession, the current database session.
    :return: An instance of CategoryRepository.
    """
    return CategoryRepository(db)
