from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    Index,
    Numeric,
    ForeignKey,
    PrimaryKeyConstraint
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.orm.base import object_state

from app.core.models import dto
from .base import Base, UTC_datetime

if TYPE_CHECKING:
    from .client import Client
    from .product import Product


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (
        Index("ix__orders_client_id", "client_id"),
        Index("ix__orders_create_date", "create_date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id", ondelete="RESTRICT")
    )
    create_date: Mapped[UTC_datetime]

    client: Mapped[Client] = relationship(
        back_populates="orders",
        # lazy="joined",
        # innerjoin=True
    )
    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan"
    )

    @classmethod
    def create(cls, client_id) -> Order:
        return cls(client_id=client_id)

    def to_dto(self) -> dto.Order:
        state = object_state(self)
        return dto.Order(
            id=self.id,
            client_id=self.client_id,
            create_date=self.create_date,
            client=self.client.to_dto() if "client" in state.dict else None,
            items=[
                i.to_dto() for i in self.items
            ] if "items" in state.dict else None,
        )


class OrderItem(Base):
    __tablename__ = "order_items"
    __table_args__ = (
        Index("ix__order_items_product", "product_id"),
        PrimaryKeyConstraint("order_id", "product_id"),
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE")
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="RESTRICT")
    )

    quantity: Mapped[int]
    unit_price: Mapped[float] = mapped_column(
        Numeric(12, 2),
        default=0.0,
    )

    order: Mapped[Order] = relationship(back_populates="items")
    product: Mapped[Product] = relationship(lazy="joined", innerjoin=True)
