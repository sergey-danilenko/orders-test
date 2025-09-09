from dishka import Provider, Scope, provide

from app.core.interfaces.adapters.product import ProductGateway
from app.core.interfaces.uow import UoW
from app.core.services.product import GetAllProduct


class ProductInteractorProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_all_products(
        self, uow: UoW, db_gateway: ProductGateway,
    ) -> GetAllProduct:
        return GetAllProduct(uow=uow, db_gateway=db_gateway)
