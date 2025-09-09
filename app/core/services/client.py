from app.core.interfaces.adapters.client import ClientGateway
from app.core.interfaces.uow import UoW
from app.core.models import dto
from app.core.common.intearctor import Interactor, InputDTO, OutputDTO


class ClientInteractor(Interactor[InputDTO, OutputDTO]):
    def __init__(self, uow: UoW, db_gateway: ClientGateway) -> None:
        self.uow = uow
        self.db_gateway = db_gateway


class GetAllClients(ClientInteractor[dto.ClientsQuery, list[dto.Client]]):
    async def __call__(self, query: dto.ClientsQuery) -> list[dto.Client]:
        clients = await self.db_gateway.get_all_clients(query)
        return clients
