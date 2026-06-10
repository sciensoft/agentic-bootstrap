"""OrderRepository protocol — the contract application depends on."""
from typing import Protocol
from uuid import UUID

from domain.model.order import Order


class OrderRepository(Protocol):
    def find(self, order_id: UUID) -> Order | None: ...
    def save(self, order: Order) -> None: ...
