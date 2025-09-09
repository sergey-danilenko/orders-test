from sqlalchemy.ext.asyncio import AsyncSession

from app.core.interfaces.adapters.product import ProductGateway
from app.infrastructure.db.gateways.base import BaseDbGateway
from app.infrastructure.db import models
from app.core.models import dto


class ProductDbDbGateway(BaseDbGateway[models.Product], ProductGateway):
    def __init__(self, session: AsyncSession):
        super().__init__(models.Product, session)

    async def get_all_products(
        self, query: dto.ProductsQuery,
    ) -> list[dto.Product]:
        products = await self._get_all(query=query)
        return [product.to_dto() for product in products]
