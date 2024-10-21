from datetime import datetime
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.infrastructure.db.models.models import Category, Product, Sale


class ReportRepository:
    """
    Repository implementation for fetching sales data using SQLAlchemy.

    This repository provides methods for generating sales reports by querying
    sales data based on product, category, and date filters. It retrieves the sales
    and their associated products, categories, and discounts.
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize the repository with a database session.

        :param db: SQLAlchemy asynchronous session for database operations.
        """
        self.db = db

    async def generate_sales_report(
        self,
        product_id: Optional[int] = None,
        product_name: Optional[str] = None,
        category_id: Optional[int] = None,
        category_name: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Sale]:
        """
        Generate a sales report based on the provided filters.

        This method constructs a dynamic SQLAlchemy query to retrieve sales that match
        the provided product, category, and date filters. It also loads related product,
        category, and discount data for each sale.

        :param product_id: The ID of the product to filter sales by.
        :param product_name: The name of the product to filter sales by.
        :param category_id: The ID of the category to filter sales by.
        :param category_name: The name of the category to filter sales by.
        :param start_date: The start date to filter sales by.
        :param end_date: The end date to filter sales by.
        :return: A list of Sale objects that match the provided filters.
        """

        query = select(Sale).options(
            selectinload(Sale.product).selectinload(Product.category),
            selectinload(Sale.product).selectinload(Product.discount),
        )

        if product_id:
            query = query.filter(Sale.product_id == product_id)

        if product_name:
            query = query.filter(Product.name.ilike(f"%{product_name}%"))

        if category_id:
            query = query.filter(Product.category_id == category_id)

        if category_name:
            query = query.join(Product.category).filter(
                Category.name.ilike(f"%{category_name}%")
            )

        if start_date:
            query = query.filter(Sale.sold_at >= start_date)
        if end_date:
            query = query.filter(Sale.sold_at <= end_date)

        result = await self.db.execute(query)
        return result.scalars().all()
