from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db import models

from sqlalchemy import select, and_, func, desc


async def get_clients_orders_sum(session: AsyncSession):
    stmt = (
        select(
            models.Client.id,
            models.Client.name,
            func.coalesce(
                func.sum(
                    models.OrderItem.unit_price * models.OrderItem.quantity),
                0
            ).label("total_amount")
        )
        .select_from(models.Client)
        .outerjoin(models.Order)
        .outerjoin(models.OrderItem)
        .group_by(models.Client.id, models.Client.name)
        .order_by(desc("total_amount"))
    )

    res = await session.execute(stmt)
    print(res.all())


async def get_categories_first_nesting_level(session: AsyncSession):
    stmt = (
        select(
            models.Category.id,
            models.Category.name,
            func.count(models.CategoryTree.depth).label("first_level_count")
        ).select_from(models.Category)
        .outerjoin(
            models.CategoryTree,
            and_(
                models.CategoryTree.ancestor_id == models.Category.id,
                models.CategoryTree.depth == 1,
            )
        )
        .group_by(models.Category.id, models.Category.name)
    )
    res = await session.execute(stmt)
    print(res.all())


async def get_top_products(session: AsyncSession):
    num_products = 5
    period = datetime.utcnow() - timedelta(days=30)

    stmt = (
        select(
            models.Product.id,
            models.Product.name.label("product"),
            models.Category.name.label("cat_name"),
            func.sum(models.OrderItem.quantity).label("total_quantity")
        ).select_from(models.Product)
        .join(models.OrderItem,
              models.OrderItem.product_id == models.Product.id)
        .join(models.Order, models.Order.id == models.OrderItem.order_id)
        .join(
            models.CategoryTree,
            and_(
                models.CategoryTree.descendant_id == models.Product.category_id,
                models.CategoryTree.depth == 1,
            )
        )
        .join(models.Category,
              models.Category.id == models.CategoryTree.ancestor_id)
        .where(models.Order.create_date >= period)
        .group_by(models.Product.id, models.Product.name, models.Category.name)
        .order_by(desc("total_quantity"))
        .limit(num_products)
    )
    res = await session.execute(stmt)
    print(res.all())
