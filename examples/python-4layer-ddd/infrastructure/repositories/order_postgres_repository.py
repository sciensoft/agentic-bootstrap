"""Postgres adapter implementing the OrderRepository protocol."""
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.model.order import Order, OrderStatus
from infrastructure.persistence.orm import OrderRow


class OrderPostgresRepository:
    def __init__(self, session: Session):
        self._session = session

    def find(self, order_id: UUID) -> Order | None:
        row = self._session.execute(
            select(OrderRow).where(OrderRow.id == order_id)
        ).scalar_one_or_none()
        return None if row is None else self._to_domain(row)

    def save(self, order: Order) -> None:
        row = self._session.get(OrderRow, order.id)
        if row is None:
            self._session.add(self._to_row(order))
        else:
            row.status = order.status.value
            row.placed_at = order.placed_at
        self._session.commit()

    @staticmethod
    def _to_domain(row: OrderRow) -> Order:
        return Order(
            id=row.id,
            customer_id=row.customer_id,
            status=OrderStatus(row.status),
            total_cents=row.total_cents,
            placed_at=row.placed_at,
        )

    @staticmethod
    def _to_row(order: Order) -> OrderRow:
        return OrderRow(
            id=order.id,
            customer_id=order.customer_id,
            status=order.status.value,
            total_cents=order.total_cents,
            placed_at=order.placed_at,
        )
