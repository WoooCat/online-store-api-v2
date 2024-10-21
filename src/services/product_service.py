from typing import List, Optional

from src.exceptions.exceptions import CategoryNotFoundError, DiscountNotFoundError, ProductNotFoundError
from src.repositories.abstract.abstract_category_repository import AbstractCategoryRepository
from src.repositories.abstract.abstract_discount_repository import AbstractDiscountRepository
from src.repositories.abstract.abstract_product_repository import AbstractProductRepository
from src.schemes.product_schemes import ProductCreateRequest, ProductResponse
from src.serializers.serializers import serialize_product_response


class ProductService:
    """
    Service class for handling business logic related to Products.
    """

    def __init__(
        self,
        product_repo: AbstractProductRepository,
        category_repo: AbstractCategoryRepository,
        discount_repo: AbstractDiscountRepository,
    ):

        """Initialize the service with repositories."""
        self.product_repo = product_repo
        self.category_repo = category_repo
        self.discount_repo = discount_repo

    async def get_all_products(
        self, cursor: Optional[int], limit: int
    ) -> List[ProductResponse]:
        """Retrieve all products with pagination."""
        products = await self.product_repo.get_all_products(cursor=cursor, limit=limit)
        return [serialize_product_response(product) for product in products]

    async def add_product(self, product_data: ProductCreateRequest) -> ProductResponse:
        """Add a new product to the system. Ensure the category exists."""
        category = await self.category_repo.get_category_by_id(product_data.category_id)
        if not category:
            raise CategoryNotFoundError(category_id=product_data.category_id)

        new_product = await self.product_repo.add_product(**product_data.dict())
        return serialize_product_response(new_product)

    async def get_product_by_id(self, product_id: int) -> ProductResponse:
        """Retrieve Product by its ID. Raise an error if not found."""
        product = await self.product_repo.get_product_by_id(product_id)
        if not product:
            raise ProductNotFoundError(product_id=product_id)
        return serialize_product_response(product)

    async def update_product(
        self, product_id: int, updated_data: dict
    ) -> ProductResponse:
        """Update a product by its ID. Raise an error if not found."""
        product = await self.product_repo.update_product(product_id, updated_data)
        if not product:
            raise ProductNotFoundError(product_id=product_id)
        return serialize_product_response(product)

    async def update_price(self, product_id: int, new_price: float) -> ProductResponse:
        """Update the price of a product. Raise an error if not found."""
        product = await self.product_repo.update_price(product_id, new_price)
        if not product:
            raise ProductNotFoundError(product_id=product_id)
        return serialize_product_response(product)

    async def delete_product(self, product_id: int) -> None:
        """Delete a product by its ID. Raise an error if not found."""
        success = await self.product_repo.delete_product(product_id)
        if not success:
            raise ProductNotFoundError(product_id=product_id)

    async def get_products_by_category(
        self, category_id: int, cursor: Optional[int], limit: int,
    ) -> List[ProductResponse]:
        """Retrieve products by category ID with pagination."""
        category = await self.category_repo.get_category_by_id(category_id)
        if not category:
            raise CategoryNotFoundError(category_id=category_id)
        products = await self.product_repo.get_products_by_category(
            category_id, cursor, limit
        )

        return [serialize_product_response(product) for product in products]

    async def add_discount_to_product(
        self, product_id: int, discount_id: int
    ) -> ProductResponse:
        """Add a discount to a product. Ensure the discount exists."""
        product = await self.product_repo.get_product_by_id(product_id)
        if not product:
            raise ProductNotFoundError(product_id=product_id)

        discount = await self.discount_repo.get_discount_by_id(discount_id)
        if not discount:
            raise DiscountNotFoundError(discount_id=discount_id)
        product = await self.product_repo.add_discount_to_product(
            product_id, discount_id
        )
        return serialize_product_response(product)

    async def remove_discount_from_product(self, product_id: int) -> ProductResponse:
        """Remove a discount from a product."""
        product = await self.product_repo.remove_discount_from_product(product_id)
        return serialize_product_response(product)
