from __future__ import annotations

from datetime import datetime
from typing import Optional

from .base import BaseDTO


class Category(BaseDTO):
    id: int
    name: str
    create_date: datetime
    parent_id: Optional[int] = None

    parent: Optional[Category] = None
    subcategories: Optional[list[Category]] = None

    @property
    def has_parent(self) -> bool:
        return self.parent_id is not None
