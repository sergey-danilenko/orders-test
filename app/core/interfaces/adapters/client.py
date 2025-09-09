from abc import abstractmethod
from typing import Protocol

from app.core.models import dto


class ClientGateway(Protocol):
    @abstractmethod
    async def get_all_clients(
        self, query: dto.ClientsQuery,
    ) -> list[dto.Client]:
        raise NotImplementedError
