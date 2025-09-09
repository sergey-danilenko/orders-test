from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.interfaces.adapters import (
    ClientGateway, OrderGateway, ProductGateway,
)
from app.infrastructure.db.gateways import (
    ClientDbDbGateway, OrderDbDbGateway, ProductDbDbGateway,
)


class GatewayProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def get_client_gateway(
        self, session: AsyncSession,
    ) -> ClientGateway:
        return ClientDbDbGateway(session=session)

    @provide
    async def get_order_gateway(
        self, session: AsyncSession,
    ) -> OrderGateway:
        return OrderDbDbGateway(session=session)

    @provide
    async def get_product_gateway(
        self, session: AsyncSession,
    ) -> ProductGateway:
        return ProductDbDbGateway(session=session)
