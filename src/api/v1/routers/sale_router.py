from fastapi import APIRouter, Depends

from src.dependencies.service_dependencies import get_sale_service
from src.schemes.sale_schemes import SaleRequest, SaleResponse
from src.services.sale_service import SaleService

router = APIRouter(prefix="/sales", tags=["sales"])


@router.post("/", response_model=SaleResponse, status_code=201)
async def buy_product(
    sale_data: SaleRequest, sale_service: SaleService = Depends(get_sale_service),
) -> SaleResponse:
    """
    Purchase a Product by specifying the product ID and quantity.

    This endpoint allows clients to buy a product by decreasing the stock and creating a sale record.
    It checks product availability and ensures that the requested quantity is in stock.
    """
    return await sale_service.buy_product(
        product_id=sale_data.product_id, quantity=sale_data.quantity
    )
