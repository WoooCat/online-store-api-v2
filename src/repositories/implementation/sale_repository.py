from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.context_managers import transaction_context
from src.infrastructure.db.models.models import Product, Sale
from src.repositories.abstract.abstract_sale_repository import AbstractSaleRepository


class SaleRepository(AbstractSaleRepository):
    """
    Concrete implementation of AbstractSaleRepository using SQLAlchemy for data persistence.

    This repository provides methods to handle sale operations, such as creating a new sale
    when a product is purchased. It interacts with the database to persist sale records.
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize the repository with DB session.
        """
        self.db = db

    async def buy_product(self, product: Product, quantity: int) -> Sale:
        """
        Create and persist a new sale record for the given product and quantity.
        """
        async with transaction_context(self.db):
            discount_id = product.discount_id
            sale = Sale(
                product_id=product.id, quantity=quantity, discount_id=discount_id
            )
            self.db.add(sale)
            await self.db.commit()
            await self.db.refresh(sale)
            return sale
