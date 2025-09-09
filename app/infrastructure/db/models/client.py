from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.base import object_state

from app.core.models import dto
from .base import Base, UTC_datetime, str_100, str_200
from .order import Order


class Client(Base):
    __tablename__ = "clients"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str_100] = mapped_column(unique=True)
    address: Mapped[str_200 | None] = mapped_column(default=None)
    create_date: Mapped[UTC_datetime]

    orders: Mapped[list[Order]] = relationship(
        back_populates="client",
        cascade="all, delete-orphan",
    )

    def to_dto(self) -> dto.Client:
        state = object_state(self)
        return dto.Client(
            id=self.id,
            name=self.name,
            create_date=self.create_date,
            address=self.address,
            orders=[
                o.to_dto() for o in self.orders
            ] if "orders" in state.dict else None,
        )
