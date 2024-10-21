from datetime import datetime
from typing import List, Optional

from src.repositories.implementation.report_repository import ReportRepository
from src.schemes.sale_schemes import SaleResponse
from src.serializers.serializers import serialize_sale_response


class ReportService:
    """
    Service layer responsible for handling business logic related to sales reports.

    This service provides functionality to fetch sales data from the repository and process it
    according to the provided filters. It applies business logic to transform raw sales data into
    the appropriate response format.
    """

    def __init__(self, report_repo: ReportRepository):
        """
        Initialize the ReportService with the necessary repository.

        :param report_repo: The repository responsible for fetching sales data.
        """
        self.report_repo = report_repo

    async def generate_sales_report(
        self,
        product_id: Optional[int] = None,
        product_name: Optional[str] = None,
        category_id: Optional[int] = None,
        category_name: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[SaleResponse]:
        """
        Retrieve a sales report based on the provided filters.

        This method coordinates the retrieval of sales data from the repository and
        processes the results to return a structured list of SaleResponse objects.

        :param product_id: The ID of the product to filter sales by.
        :param product_name: The name of the product to filter sales by.
        :param category_id: The ID of the category to filter sales by.
        :param category_name: The name of the category to filter sales by.
        :param start_date: The start date to filter sales by.
        :param end_date: The end date to filter sales by.
        :return: A list of SaleResponse objects containing the filtered sales data.
        """

        sales = await self.report_repo.generate_sales_report(
            product_id=product_id,
            product_name=product_name,
            category_id=category_id,
            category_name=category_name,
            start_date=start_date,
            end_date=end_date,
        )
        return [serialize_sale_response(sale, sale.product) for sale in sales]
