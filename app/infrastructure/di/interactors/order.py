from dishka import Provider, Scope, provide

from app.core.interfaces.adapters.order import OrderGateway
from app.core.interfaces.uow import UoW
from app.core.services.order import (
    GetOrderById,
    GetAllOrders,
    CreateOrder,
    UpdateOrder,
    DeleteOrder,
)


class OrderInteractorProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_by_id(
        self, uow: UoW, db_gateway: OrderGateway,
    ) -> GetOrderById:
        return GetOrderById(uow=uow, db_gateway=db_gateway)

    @provide
    def get_all_orders(
        self, uow: UoW, db_gateway: OrderGateway,
    ) -> GetAllOrders:
        return GetAllOrders(uow=uow, db_gateway=db_gateway)

    @provide
    def create_order(
        self, uow: UoW, db_gateway: OrderGateway,
    ) -> CreateOrder:
        return CreateOrder(uow=uow, db_gateway=db_gateway)

    @provide
    def update_order(
        self, uow: UoW, db_gateway: OrderGateway,
    ) -> UpdateOrder:
        return UpdateOrder(uow=uow, db_gateway=db_gateway)

    @provide
    def delete_order(
        self, uow: UoW, db_gateway: OrderGateway,
    ) -> DeleteOrder:
        return DeleteOrder(uow=uow, db_gateway=db_gateway)
