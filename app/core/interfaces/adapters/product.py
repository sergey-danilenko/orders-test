from abc import abstractmethod
from typing import Protocol

from app.core.models import dto


class ProductGateway(Protocol):
    @abstractmethod
    async def get_all_products(
        self, query: dto.ProductsQuery,
    ) -> list[dto.Product]:
        raise NotImplementedError
