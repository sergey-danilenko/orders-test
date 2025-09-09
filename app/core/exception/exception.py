from .base import AppException


class GatewayError(AppException):
    notify = "Base gateway error"


class OrderException(GatewayError):
    notify = "Base order exception"


class OrderNotFound(OrderException):
    notify = "Order not found"


class OutOfStockOrUnavailable(OrderException):
    notify = "The product/s is out of stock or unavailable"


class ClientException(GatewayError):
    notify = "Base Client Exception"


class ClientNotFound(ClientException):
    notify = "Client not found"


class ProductNotFound(GatewayError):
    notify = "Product not found"
