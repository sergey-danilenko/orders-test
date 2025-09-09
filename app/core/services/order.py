from app.core.exception.exception import OutOfStockOrUnavailable, OrderNotFound, \
    ClientNotFound
from app.core.interfaces.adapters.order import OrderGateway
from app.core.interfaces.uow import UoW
from app.core.models import dto
from app.core.common.intearctor import Interactor, InputDTO, OutputDTO


class OrderInteractor(Interactor[InputDTO, OutputDTO]):
    def __init__(self, uow: UoW, db_gateway: OrderGateway) -> None:
        self.uow = uow
        self.db_gateway = db_gateway


class GetOrderById(OrderInteractor[int, dto.Order]):
    async def __call__(self, order_id: int) -> dto.Order:
        order = await self.db_gateway.get_by_id(order_id)
        return order


class GetAllOrder(OrderInteractor[dto.OrdersQuery, list[dto.Order]]):
    async def __call__(self, query: dto.OrdersQuery) -> list[dto.Order]:
        orders = await self.db_gateway.get_all_orders(query)
        return orders


class CreateOrder(OrderInteractor[dto.CreateOrder, dto.Order]):
    async def __call__(self, query: dto.CreateOrder) -> dto.Order:
        try:
            order = await self.db_gateway.create_order(query)
            await self.uow.commit()
            return order
        except (ClientNotFound, OutOfStockOrUnavailable) as e:
            await self.uow.rollback()
            raise


class UpdateOrder(OrderInteractor[dto.UpdateOrder, dto.Order]):
    async def __call__(self, query: dto.UpdateOrder) -> dto.Order:
        try:
            order = await self.db_gateway.update_order(query=query)
            await self.uow.commit()
            return order
        except (OrderNotFound, OutOfStockOrUnavailable) as e:
            await self.uow.rollback()
            raise


class DeleteOrder(OrderInteractor[int, bool]):
    async def __call__(self, order_id: int) -> bool:
        res = await self.db_gateway.delete_order(order_id=order_id)
        await self.uow.commit()
        return res
