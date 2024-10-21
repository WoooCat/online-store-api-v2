from fastapi import Depends

from src.dependencies.repository_dependencies import get_category_repository
from src.repositories.implementation.category_repository import CategoryRepository
from src.services.category_service import CategoryService


def get_category_service(
    category_repo: CategoryRepository = Depends(get_category_repository),
) -> CategoryService:
    """
    Returns a CategoryService instance, injecting the CategoryRepository dependency.

    :param category_repo: The CategoryRepository instance.
    :return: An instance of CategoryService.
    """
    return CategoryService(category_repo)
