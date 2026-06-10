"""Service tested against in-memory fakes — no DB needed, no mocks for internals."""
from datetime import datetime, timezone
from uuid import UUID, uuid4

import pytest

from application.services.order_service import OrderNotFoundError, OrderService
from domain.model.order import Order, OrderAlreadyPlacedError, OrderStatus


class InMemoryOrderRepository:
    def __init__(self) -> None:
        self._store: dict[UUID, Order] = {}

    def find(self, order_id: UUID) -> Order | None:
        return self._store.get(order_id)

    def save(self, order: Order) -> None:
        self._store[order.id] = order


class FrozenClock:
    def __init__(self, now: datetime) -> None:
        self._now = now

    def now(self) -> datetime:
        return self._now


@pytest.fixture
def now() -> datetime:
    return datetime(2026, 6, 10, 12, 0, tzinfo=timezone.utc)


@pytest.fixture
def draft_order() -> Order:
    return Order(
        id=uuid4(),
        customer_id=uuid4(),
        status=OrderStatus.DRAFT,
        total_cents=10_00,
        placed_at=None,
    )


def test_place_marks_order_as_placed_and_stamps_time(now, draft_order):
    repo = InMemoryOrderRepository()
    repo.save(draft_order)
    service = OrderService(orders=repo, clock=FrozenClock(now))

    placed = service.place(draft_order.id)

    assert placed.status == OrderStatus.PLACED
    assert placed.placed_at == now
    assert repo.find(draft_order.id) == placed


def test_place_raises_when_order_not_found(now):
    service = OrderService(orders=InMemoryOrderRepository(), clock=FrozenClock(now))

    with pytest.raises(OrderNotFoundError):
        service.place(uuid4())


def test_place_raises_when_already_placed(now, draft_order):
    repo = InMemoryOrderRepository()
    repo.save(draft_order)
    service = OrderService(orders=repo, clock=FrozenClock(now))
    service.place(draft_order.id)

    with pytest.raises(OrderAlreadyPlacedError):
        service.place(draft_order.id)
