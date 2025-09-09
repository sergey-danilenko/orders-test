from sqlalchemy import update, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exception.exception import (
    OrderNotFound,
    OutOfStockOrUnavailable, ClientNotFound,
)
from app.core.interfaces.adapters.order import OrderGateway
from app.infrastructure.db.gateways.base import BaseDbGateway
from app.infrastructure.db import models
from app.core.models import dto


class OrderDbDbGateway(BaseDbGateway[models.Order], OrderGateway):
    def __init__(self, session: AsyncSession):
        super().__init__(models.Order, session)

    async def get_by_id(self, order_id: int) -> dto.Order:
        if org := await self._get_by_id(order_id):
            return org.to_dto()

    async def get_all_orders(
        self, query: dto.OrdersQuery,
    ) -> list[dto.Order]:
        orders = await self._get_all(query=query)
        return [order.to_dto() for order in orders]

    async def create_order(self, query: dto.CreateOrder) -> dto.Order:
        order = self.model.create(client_id=query.client_id)
        try:
            self._add(order)
            await self._flush()
        except IntegrityError:
            raise ClientNotFound(client_id=query.client_id)

        await self._upsert_order_items(order.id, query.products)
        return order.to_dto()

    async def update_order(
        self, query: dto.UpdateOrder,
    ) -> dto.Order:
        order = await self._get_by_id(id_=query.order_id)
        if not order:
            raise OrderNotFound(order_id=query.order_id)

        await self._upsert_order_items(order.id, query.products)
        return order.to_dto()

    async def _upsert_order_items(
        self,
        order_id: int,
        products: list[dto.ProductInOrder]
    ):
        updated_products = []
        for p in products:
            stmt = (
                update(models.Product)
                .where(
                    and_(
                        models.Product.id == p.product_id,
                        models.Product.stock_quantity >= p.quantity,
                    )
                )
                .values(
                    stock_quantity=models.Product.stock_quantity - p.quantity)
                .returning(models.Product.id, models.Product.price)
            )
            res = (await self.session.execute(stmt)).first()
            if not res:
                raise OutOfStockOrUnavailable(
                    product_id=p.product_id,
                    quantity=p.quantity,
                )

            product_id, price = res
            updated_products.append(
                {
                    "order_id": order_id,
                    "product_id": product_id,
                    "quantity": p.quantity,
                    "unit_price": price,
                }
            )

        stmt = (self.insert(models.OrderItem).values(updated_products))
        stmt = stmt.on_conflict_do_update(
            index_elements=(
                models.OrderItem.order_id,
                models.OrderItem.product_id,
            ),
            set_={
                "quantity": stmt.excluded.quantity + models.OrderItem.quantity,
            }
        )
        await self.session.execute(stmt)

    async def delete_order(
        self, order_id: int,
    ) -> bool:
        order = await self._get_by_id(order_id)
        if order:
            await self.session.delete(order)
        return order is not None
