from .client import ClientInteractorProvider
from .order import OrderInteractorProvider
from .product import ProductInteractorProvider


def get_interactor_providers():
    return [
        ClientInteractorProvider(),
        OrderInteractorProvider(),
        ProductInteractorProvider(),
    ]
