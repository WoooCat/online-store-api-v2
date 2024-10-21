from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.infrastructure.db.context_managers import transaction_context
from src.infrastructure.db.models.models import Category, Product
from src.repositories.abstract.abstract_product_repository import AbstractProductRepository
from src.schemes.product_schemes import ProductCreateRequest


class ProductRepository(AbstractProductRepository):
    """Implementation of Product repository using SQLAlchemy DB."""

    def __init__(self, db: AsyncSession):
        """Init database session."""
        self.db = db

    async def get_all_products(
        self, cursor: Optional[int], limit: int = 10
    ) -> List[Product]:
        """Retrieve all Products with pagination form DB."""
        query = select(Product)
        if cursor is not None:
            query = query.filter(Product.id > cursor)
        query = query.order_by(Product.id).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().fetchmany(limit)

    async def add_product(self, **product_data: ProductCreateRequest) -> Product:
        """Add new Product to DB."""
        async with transaction_context(self.db):
            product = Product(**product_data)

            self.db.add(product)
            await self.db.commit()
            await self.db.refresh(product)
        return product

    async def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Retrieve a Product by its ID from DB."""
        query = select(Product).filter(Product.id == product_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def update_product(self, product_id: int, updated_data: dict) -> Product:
        """Update a Product by its ID in DB."""
        async with transaction_context(self.db):
            product = await self.get_product_by_id(product_id)
            if product:
                self._update_product_fields(product, updated_data)
                await self.db.commit()
                await self.db.refresh(product)
        return product

    async def update_price(self, product_id: int, new_price: float) -> Product:
        """Update the price of a product by its ID in DB."""
        async with transaction_context(self.db):
            product = await self.get_product_by_id(product_id)
            if product:
                product.price = new_price
                await self.db.commit()
                await self.db.refresh(product)
            return product

    async def delete_product(self, product_id: int) -> bool:
        """Delete a product by its ID from DB."""
        async with transaction_context(self.db):
            product = await self.get_product_by_id(product_id)
            if not product:
                return False
            await self.db.delete(product)
            await self.db.commit()
            return True

    async def get_products_by_category(
        self, category_id: int, cursor: Optional[int], limit: int = 10
    ) -> List[Product]:
        """Retrieve products by category ID with pagination from DB."""
        query = select(Product).filter(
            (Product.category_id == category_id)
            | (Product.category.has(Category.parent_id == category_id)),
            Product.stock > 0,
        )

        if cursor is not None:
            query = query.filter(Product.id > cursor)
        query = query.order_by(Product.id).limit(limit)

        result = await self.db.execute(query)

        return result.scalars().fetchmany(limit)

    async def add_discount_to_product(
        self, product_id: int, discount_id: int
    ) -> Product:
        """Add a discount to a product by product_id and discount_id in DB."""
        async with transaction_context(self.db):
            product = await self.get_product_by_id(product_id)
            product.discount_id = discount_id
            await self.db.commit()
            await self.db.refresh(product)
        return product

    async def remove_discount_from_product(self, product_id: int) -> Product:
        """Remove a discount from a product by its ID in DB."""
        async with transaction_context(self.db):
            product = await self.get_product_by_id(product_id)
            product.discount_id = None
            await self.db.commit()
            await self.db.refresh(product)
        return product

    async def update_product_stock(self, product_id: int, new_stock: int) -> Product:
        """Update the stock quantity of a product."""
        async with transaction_context(self.db):
            product = await self.get_product_by_id(product_id)
            if product:
                product.stock = new_stock
                await self.db.commit()
                await self.db.refresh(product)
        return product

    @staticmethod
    def _update_product_fields(product: Product, updated_data: dict) -> None:
        """Update product fields for Product."""
        for key, value in updated_data.items():
            setattr(product, key, value)
