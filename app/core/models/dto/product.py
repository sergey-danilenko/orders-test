from datetime import datetime
from typing import Optional

from .base import BaseDTO
from .categories import Category


class Product(BaseDTO):
    id: int
    name: str
    category_id: int
    stock_quantity: int
    price: float
    create_date: datetime

    category: Optional[Category] = None
