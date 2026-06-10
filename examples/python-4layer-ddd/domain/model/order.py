"""Order domain model. Pure types; zero outward imports."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID


class OrderStatus(str, Enum):
    DRAFT = "draft"
    PLACED = "placed"
    FULFILLED = "fulfilled"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class Order:
    id: UUID
    customer_id: UUID
    status: OrderStatus
    total_cents: int
    placed_at: datetime | None

    def place(self, when: datetime) -> "Order":
        if self.status != OrderStatus.DRAFT:
            raise OrderAlreadyPlacedError(self.id)
        return Order(
            id=self.id,
            customer_id=self.customer_id,
            status=OrderStatus.PLACED,
            total_cents=self.total_cents,
            placed_at=when,
        )


class OrderAlreadyPlacedError(Exception):
    def __init__(self, order_id: UUID):
        super().__init__(f"Order {order_id} already placed")
        self.order_id = order_id
