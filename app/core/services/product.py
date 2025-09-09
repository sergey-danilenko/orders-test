from app.core.interfaces.adapters.product import ProductGateway
from app.core.interfaces.uow import UoW
from app.core.models import dto
from app.core.common.intearctor import Interactor, InputDTO, OutputDTO


class ProductInteractor(Interactor[InputDTO, OutputDTO]):
    def __init__(self, uow: UoW, db_gateway: ProductGateway) -> None:
        self.uow = uow
        self.db_gateway = db_gateway


class GetAllProduct(ProductInteractor[dto.ProductsQuery, list[dto.Product]]):
    async def __call__(self, query: dto.ProductsQuery) -> list[dto.Product]:
        products = await self.db_gateway.get_all_products(query)
        return products
