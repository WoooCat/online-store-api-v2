from typing import List

from fastapi import APIRouter, Depends

from src.dependencies.service_dependencies import get_reservation_service
from src.schemes.pagination_schemes import PaginationParams
from src.schemes.reservation_schemes import ReservationRequest, ReservationResponse
from src.services.reservation_service import ReservationService

router = APIRouter(prefix="/reservation", tags=["reservation"])


@router.post("/", response_model=ReservationResponse, status_code=201)
async def reserve_product(
    reservation_data: ReservationRequest,
    reservation_service: ReservationService = Depends(get_reservation_service),
) -> ReservationResponse:
    """
    Reserve a product by specifying the product ID and quantity.

    This endpoint allows clients to reserve a specific quantity of a product.
    The stock is checked to ensure that the requested quantity is available.
    """
    return await reservation_service.reserve_product(
        product_id=reservation_data.product_id, quantity=reservation_data.quantity,
    )


@router.get("/", response_model=List[ReservationResponse])
async def get_all_reservations(
    reservation_service: ReservationService = Depends(get_reservation_service),
    pagination: PaginationParams = Depends(),
) -> List[ReservationResponse]:
    """
    Retrieve a paginated list of all reservations.

    Allows fetching a list of reservations, supporting pagination for efficient data retrieval.
    """
    return await reservation_service.get_all_reservations(
        cursor=pagination.cursor, limit=pagination.limit
    )


@router.get("/{reservation_id}", response_model=ReservationResponse)
async def get_reservation_by_id(
    reservation_id: int,
    reservation_service: ReservationService = Depends(get_reservation_service),
) -> ReservationResponse:
    """
    Get a reservation by its ID.

    Fetches a specific reservation based on its unique identifier.
    """
    return await reservation_service.get_reservation_by_id(reservation_id)


@router.get("/product/{product_id}", response_model=List[ReservationResponse])
async def get_reservations_by_product_id(
    product_id: int,
    reservation_service: ReservationService = Depends(get_reservation_service),
    pagination: PaginationParams = Depends(),
) -> List[ReservationResponse]:
    """
    Retrieve reservations for a specific product by product ID.

    Allows fetching reservations associated with a particular product.
    Supports pagination for efficient data retrieval.
    """
    return await reservation_service.get_reservations_by_product_id(
        product_id, cursor=pagination.cursor, limit=pagination.limit,
    )


@router.patch("/{reservation_id}/cancel", status_code=204)
async def cancel_reservation(
    reservation_id: int,
    reservation_service: ReservationService = Depends(get_reservation_service),
) -> None:
    """
    Cancel an active reservation by its ID.

    Marks a reservation as inactive and restores the reserved stock to the product.
    """
    return await reservation_service.cancel_reservation(reservation_id)
