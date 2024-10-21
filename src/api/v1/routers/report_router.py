from typing import List

from fastapi import APIRouter, Depends

from src.dependencies.service_dependencies import get_report_service
from src.schemes.sale_schemes import SaleFilterRequest, SaleResponse
from src.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/sales", response_model=List[SaleResponse])
async def get_sales_report(
    filters: SaleFilterRequest = Depends(),
    report_service: ReportService = Depends(get_report_service),
) -> List[SaleResponse]:
    """
    Retrieve Sales report based on the provided filters.

    This endpoint allows clients to generate a sales report by filtering sales data
    based on product ID, product name, category, and date range.
    The results are returned in a structured response format that includes product and sales details.
    """
    return await report_service.generate_sales_report(
        product_id=filters.product_id,
        product_name=filters.product_name,
        category_id=filters.category_id,
        category_name=filters.category_name,
        start_date=filters.start_date,
        end_date=filters.end_date,
    )
