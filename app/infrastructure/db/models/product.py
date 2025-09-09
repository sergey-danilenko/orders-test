from __future__ import annotations

from sqlalchemy import ForeignKey, Numeric, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.base import object_state

from app.core.models import dto
from .base import Base, UTC_datetime, str_100
from .categories import Category


class Product(Base):
    __tablename__ = "products"
    __mapper_args__ = {"eager_defaults": True}
    __table_args__ = (
        Index("ix__products_category_id", "category_id"),
        UniqueConstraint(
            "category_id", "name",
            name="uq__products_category_name_model",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str_100]
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"),
    )
    stock_quantity: Mapped[int] = mapped_column(default=0)
    price: Mapped[float] = mapped_column(
        Numeric(12, 2),
        default=0.0,
    )
    create_date: Mapped[UTC_datetime]

    category: Mapped[Category] = relationship()

    def to_dto(self) -> dto.Product:
        state = object_state(self)
        return dto.Product(
            id=self.id,
            name=self.name,
            category_id=self.category_id,
            stock_quantity=self.stock_quantity,
            price=self.price,
            create_date=self.create_date,
            category=self.category.to_dto() if "category" in state.dict else None,
        )
