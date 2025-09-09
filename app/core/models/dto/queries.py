from .base import BaseDTO
from .. import enums


class ProductInOrder(BaseDTO):
    product_id: int
    quantity: int


class CreateOrder(BaseDTO):
    client_id: int
    products: list[ProductInOrder]


class UpdateOrder(BaseDTO):
    order_id: int
    products: list[ProductInOrder]


class BaseQuery(BaseDTO):
    limit: int = 0
    offset: int = 0
    order: str = enums.SortedBy.CREATE_DATE
    direction: str = enums.Direction.DESC


class OrdersQuery(BaseQuery):
    pass


class ClientsQuery(BaseQuery):
    pass


class ProductsQuery(BaseQuery):
    pass
