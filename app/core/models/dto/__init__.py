from .base import BaseDTO
from .categories import Category
from .client import Client
from .order import Order, OrderItem
from .product import Product
from .queries import (
    ProductInOrder,
    CreateOrder,
    UpdateOrder,
    BaseQuery,
    OrdersQuery,
    ClientsQuery,
    ProductsQuery,
)

Category.model_rebuild()
Client.model_rebuild()
Order.model_rebuild()
OrderItem.model_rebuild()
Product.model_rebuild()

__all__ = (
    "BaseDTO",
    "BaseQuery",
    "Category",
    "Client",
    "ClientsQuery",
    "CreateOrder",
    "Order",
    "OrderItem",
    "OrdersQuery",
    "Product",
    "ProductInOrder",
    "ProductsQuery",
    "UpdateOrder",
)
