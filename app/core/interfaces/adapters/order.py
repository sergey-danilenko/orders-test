from abc import abstractmethod
from typing import Protocol

from app.core.models import dto


class OrderGateway(Protocol):
    @abstractmethod
    async def get_by_id(
        self, order_id: int,
    ) -> dto.Order:
        raise NotImplementedError

    @abstractmethod
    async def get_all_orders(self, query: dto.OrdersQuery) -> list[dto.Order]:
        raise NotImplementedError

    @abstractmethod
    async def create_order(self, query: dto.CreateOrder) -> dto.Order:
        raise NotImplementedError

    @abstractmethod
    async def update_order(self, query: dto.UpdateOrder) -> dto.Order:
        raise NotImplementedError

    @abstractmethod
    async def delete_order(self, order_id: int) -> bool:
        raise NotImplementedError
