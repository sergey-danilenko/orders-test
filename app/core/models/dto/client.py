from datetime import datetime
from typing import Optional

from .base import BaseDTO
from .order import Order


class Client(BaseDTO):
    id: int
    name: str
    create_date: datetime
    address: Optional[str] = None

    orders: Optional[list["Order"]] = None

    # class Config:
    #     json_schema_extra = {
    #         "example": {
    #             "id": 1,
    #             "name": "Название компании",
    #             "create_date": "2025-09-09T06:35:28",
    #             "address": "Адрес компании",
    #             "orders": None
    #         }
    #     }
