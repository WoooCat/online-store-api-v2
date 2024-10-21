from src.exceptions.exceptions import NotEnoughStockError, ProductNotFoundError
from src.repositories.abstract.abstract_product_repository import AbstractProductRepository
from src.repositories.abstract.abstract_sale_repository import AbstractSaleRepository
from src.schemes.sale_schemes import SaleResponse
from src.serializers.serializers import serialize_sale_response


class SaleService:
    """
    Service layer responsible for implementing business logic related to sales.

    This service coordinates the process of purchasing products, adjusting stock levels,
    and creating sale records. It validates product availability and applies the necessary
    operations to update both the product's stock and the sales records.
    """

    def __init__(
        self, sale_repo: AbstractSaleRepository, product_repo: AbstractProductRepository
    ):
        """
        Initialize the SaleService with the necessary repositories.

        :param sale_repo: Repository for managing sales.
        :param product_repo: Repository for managing products and stock.
        """
        self.sale_repo = sale_repo
        self.product_repo = product_repo

    async def buy_product(self, product_id: int, quantity: int) -> SaleResponse:
        """
        Purchase a product by decreasing its stock and creating a sale record.
        """
        product = await self.product_repo.get_product_by_id(product_id)
        if not product:
            raise ProductNotFoundError(product_id=product_id)

        if product.stock < quantity:
            raise NotEnoughStockError(product_id=product_id)

        product.stock -= quantity
        await self.product_repo.update_product(product_id, {"stock": product.stock})

        sale = await self.sale_repo.buy_product(product, quantity)

        return serialize_sale_response(product=product, sale=sale)
