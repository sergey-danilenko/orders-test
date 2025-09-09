from dishka import Provider, Scope, provide

from app.core.interfaces.adapters.client import ClientGateway
from app.core.interfaces.uow import UoW
from app.core.services.client import GetAllClients


class ClientInteractorProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_all_clients(
        self, uow: UoW, db_gateway: ClientGateway,
    ) -> GetAllClients:
        return GetAllClients(uow=uow, db_gateway=db_gateway)
