from datetime import datetime
from typing import Optional, TYPE_CHECKING

from .base import BaseDTO

if TYPE_CHECKING:
    from .client import Client
    from .product import Product


class Order(BaseDTO):
    id: int
    client_id: int
    create_date: datetime

    client: Optional["Client"] = None
    items: Optional[list["OrderItem"]] = None


class OrderItem(BaseDTO):
    order_id: int
    product_id: int
    quantity: int
    unit_price: float

    order: Optional["Order"] = None
    product: Optional["Product"] = None
