from sqlalchemy.ext.asyncio import AsyncSession

from app.core.interfaces.adapters.client import ClientGateway
from app.infrastructure.db.gateways.base import BaseDbGateway
from app.infrastructure.db import models
from app.core.models import dto


class ClientDbDbGateway(BaseDbGateway[models.Client], ClientGateway):
    def __init__(self, session: AsyncSession):
        super().__init__(models.Client, session)

    async def get_all_clients(
        self, query: dto.ClientsQuery,
    ) -> list[dto.Client]:
        clients = await self._get_all(query=query)
        return [client.to_dto() for client in clients]
