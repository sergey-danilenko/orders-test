from __future__ import annotations

from sqlalchemy import (
    Index,
    ForeignKey,
    UniqueConstraint,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.orm.base import object_state

from app.core.models import dto
from .base import Base, UTC_datetime, str_100


class Category(Base):
    __tablename__ = "categories"
    __mapper_args__ = {"eager_defaults": True}
    __table_args__ = (
        Index("ix__categories_name", "name"),
        Index("ix__categories_parent_id", "parent_id"),
        UniqueConstraint(
            "parent_id", "name",
            name="uq__categories__parent_name",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str_100]
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        default=None,
    )
    create_date: Mapped[UTC_datetime]

    parent: Mapped[Category | None] = relationship(
        back_populates="subcategories", remote_side=[id]
    )
    subcategories: Mapped[list[Category]] = relationship(
        back_populates="parent", cascade="all, delete"
    )

    def to_dto(self) -> dto.Category:
        state = object_state(self)
        return dto.Category(
            id=self.id,
            name=self.name,
            create_date=self.create_date,
            parent_id=self.parent_id,
            parent=self.parent.to_dto() if "parent" in state.dict else None,
            subcategories=[
                c.to_dto() for c in self.subcategories
            ] if "subcategories" in state.dict else None
        )


class CategoryTree(Base):
    __tablename__ = "category_trees"
    __mapper_args__ = {"eager_defaults": True}
    __table_args__ = (
        Index("ix__cc_ancestor", "ancestor_id"),
        Index("ix__cc_descendant", "descendant_id"),
        PrimaryKeyConstraint("ancestor_id", "descendant_id"),
    )

    ancestor_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE")
    )
    descendant_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE")
    )
    depth: Mapped[int]
