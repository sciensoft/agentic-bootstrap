"""OrderService — application layer. No I/O, no framework imports."""
from datetime import datetime
from uuid import UUID

from domain.interfaces.order_repository import OrderRepository
from domain.model.order import Order


class OrderNotFoundError(Exception):
    pass


class OrderService:
    def __init__(self, orders: OrderRepository, clock: "Clock"):
        self._orders = orders
        self._clock = clock

    def place(self, order_id: UUID) -> Order:
        order = self._orders.find(order_id)
        if order is None:
            raise OrderNotFoundError(order_id)
        placed = order.place(self._clock.now())
        self._orders.save(placed)
        return placed


class Clock:
    def now(self) -> datetime: ...
