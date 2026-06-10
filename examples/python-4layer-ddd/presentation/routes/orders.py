"""HTTP route — orchestrates, never computes."""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from application.container import get_order_service
from application.services.order_service import OrderNotFoundError, OrderService
from domain.model.order import OrderAlreadyPlacedError

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/{order_id}/place")
def place_order(
    order_id: UUID,
    service: OrderService = Depends(get_order_service),
) -> dict:
    try:
        order = service.place(order_id)
    except OrderNotFoundError:
        raise HTTPException(404, "order not found")
    except OrderAlreadyPlacedError:
        raise HTTPException(409, "order already placed")
    return {"id": str(order.id), "status": order.status.value, "placed_at": order.placed_at}
