from fastapi import Depends

from src.dependencies.repository_dependencies import get_category_repository, get_product_repository, \
    get_discount_repository, get_reservation_repository
from src.repositories.implementation.category_repository import CategoryRepository
from src.repositories.implementation.discount_repository import DiscountRepository
from src.repositories.implementation.product_repository import ProductRepository
from src.repositories.implementation.reservation_repository import ReservationRepository
from src.services.category_service import CategoryService
from src.services.discount_service import DiscountService
from src.services.product_service import ProductService
from src.services.reservation_service import ReservationService


def get_category_service(
    category_repo: CategoryRepository = Depends(get_category_repository),
) -> CategoryService:
    """
    Returns a CategoryService instance, injecting the CategoryRepository dependency.

    :param category_repo: The CategoryRepository instance.
    :return: An instance of CategoryService.
    """
    return CategoryService(category_repo)


def get_product_service(
    product_repo: ProductRepository = Depends(get_product_repository),
    category_repo: CategoryRepository = Depends(get_category_repository),
    discount_repo: DiscountRepository = Depends(get_discount_repository),
) -> ProductService:
    """
    Returns a ProductService instance, injecting the ProductRepository, CategoryRepository,
    and DiscountRepository dependencies.

    :param product_repo: The ProductRepository instance.
    :param category_repo: The CategoryRepository instance.
    :param discount_repo: The DiscountRepository instance.
    :return: An instance of ProductService.
    """
    return ProductService(product_repo, category_repo, discount_repo)


def get_discount_service(
    discount_repo: DiscountRepository = Depends(get_discount_repository),
) -> DiscountService:
    """
    Returns a DiscountService instance, injecting the DiscountRepository dependency.

    :param discount_repo: The DiscountRepository instance.
    :return: An instance of DiscountService.
    """
    return DiscountService(discount_repo)


def get_reservation_service(
    reservation_repo: ReservationRepository = Depends(get_reservation_repository),
    product_repo: ProductRepository = Depends(get_product_repository),
) -> ReservationService:
    """
     Returns a ReservationService instance, injecting the ReservationRepository and ProductRepository dependencies.

     :param reservation_repo: The ReservationRepository instance.
     :param product_repo: The ProductRepository instance.
     :return: An instance of ReservationService.
     """
    return ReservationService(reservation_repo, product_repo)
