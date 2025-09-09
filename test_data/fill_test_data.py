import asyncio
import json
import random

from pathlib import Path
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession

from app.common.config import Config, Paths
from app.common.config import load_config
from app.common.config import get_paths
from app.common.db_type import DbType

from app.infrastructure.db.factory import create_engine, create_session_maker
from app.infrastructure.db import models

from sqlalchemy import select, update, and_

random.seed(42)

paths: Paths = get_paths()
config: Config = load_config(paths)

match config.db.type:
    case DbType.SQLITE:
        from sqlalchemy.dialects.sqlite import insert
    case DbType.POSTGRESQL:
        from sqlalchemy.dialects.postgresql import insert


def get_data(path: Path) -> dict | list:
    with open(paths.app_dir / "test_data" / path, "r", encoding="utf-8") as file:
        return json.loads(file.read())


async def fill_order_items(
    session: AsyncSession,
    orders_map: dict[int, int],
    selected_products: dict[int, Sequence[models.Product]],
) -> None:
    order_items = []
    for client_id, products in selected_products.items():
        order_id = orders_map[client_id]
        for product in products:
            order_items.append(
                {
                    "order_id": order_id,
                    "product_id": product.id,
                    "quantity": 1,
                    "unit_price": product.price,
                }
            )

    stmt = insert(models.OrderItem).values(order_items)
    stmt = stmt.on_conflict_do_nothing(
        index_elements=(
            models.OrderItem.order_id,
            models.OrderItem.product_id,
        )
    ).returning(models.OrderItem)

    new_items = (await session.scalars(stmt)).all()

    if new_items:
        product_ids = [item.product_id for item in new_items]
        update_stmt = (
            update(models.Product)
            .where(
                and_(
                    models.Product.id.in_(product_ids),
                    models.Product.stock_quantity > 0,
                )
            )
            .values(stock_quantity=models.Product.stock_quantity - 1)
            .returning(models.Product.id)
        )
        await session.execute(update_stmt)


async def fill_orders(
    session: AsyncSession,
    clients: Sequence[models.Client],
    products: Sequence[models.Product],
) -> None:

    selected_clients: Sequence[models.Client] = random.sample(clients, 6)
    selected_products = {
        c.id: random.sample(products, random.randint(1, 4))
        for c in selected_clients
    }

    orders = []
    for client_id in selected_products.keys():
        stmt = select(models.Order).where(models.Order.client_id == client_id)

        if not (order := (await session.scalars(stmt)).first()):
            stmt = insert(models.Order).values(
                [{"client_id": client_id}]
            ).returning(models.Order)
            order = (await session.scalars(stmt)).first()

        orders.append(order)

    orders_map = {o.client_id: o.id for o in orders}
    await fill_order_items(session, orders_map, selected_products)


async def fill_clients(session: AsyncSession) -> Sequence[models.Client]:
    data = get_data(Path("clients.json"))

    stmt = insert(models.Client).values(data)
    stmt = stmt.on_conflict_do_update(
        index_elements=(models.Client.name,),
        set_={"address": stmt.excluded.address}
    ).returning(models.Client)

    saved_clients = (await session.scalars(stmt)).all()
    return saved_clients


async def fill_products(
    session: AsyncSession,
    categories: Sequence[models.Category],
) -> Sequence[models.Product]:
    data = get_data(Path("products.json"))

    cat_map = {cat.name: cat.id for cat in categories}
    for product in data:
        cat_id = cat_map.get(product.pop("subcategory"))
        product.update({"category_id": cat_id})

    stmt = insert(models.Product).values(data)
    stmt = stmt.on_conflict_do_update(
        index_elements=(
            models.Product.name,
            models.Product.category_id,
        ),
        set_={"price": stmt.excluded.price}
    ).returning(models.Product)

    saved_products = (await session.scalars(stmt)).all()
    return saved_products


async def fill_categories(session: AsyncSession) -> Sequence[models.Category]:
    async def create_activities(
        data: dict, parent: models.Category | None = None,
    ) -> None:
        for name, subcategories in data.items():
            stmt = select(models.Category).where(
                models.Category.name == name,
                (models.Category.parent_id == parent.id) if parent
                else (models.Category.parent_id.is_(None))
            )
            if not (category := (await session.scalars(stmt)).first()):
                stmt = insert(models.Category).values(
                    [
                        {
                            "name": name,
                            "parent_id": parent.id if parent else None,
                        },
                    ]
                ).returning(models.Category)

                category = (await session.scalars(stmt)).first()
            added_categories.append(category)
            if isinstance(subcategories, list):
                for item in subcategories:
                    await create_activities(item, parent=category)

    added_categories: list[models.Category] = []
    await create_activities(
        get_data(Path("categories.json"))
    )
    return added_categories


async def fill_test_data(session: AsyncSession):
    categories = await fill_categories(session)
    products = await fill_products(session, categories)
    clients = await fill_clients(session)
    await fill_orders(session, clients, products)


async def main():
    engine: AsyncEngine = create_engine(config.db, echo=True)
    pool: async_sessionmaker[AsyncSession] = create_session_maker(engine)

    async with pool() as session:
        await fill_test_data(session)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
