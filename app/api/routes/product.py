from http import HTTPMethod

from dishka.integrations.fastapi import inject, FromDishka
from fastapi import APIRouter, Query

from app.api.docs.common import (
    UNAUTHORIZED_ERROR, VALIDATION_ERROR
)
from app.api.docs.responses.product import PRODUCT_LIST
from app.core.models import dto, enums
from app.core.services import GetAllProduct


@inject
async def get_all_products(
    interactor: FromDishka[GetAllProduct],
    limit: int = Query(default=5, description="Количество товара в ответе"),
    offset: int = Query(
        default=0,
        description="Смещение относительно первого товара",
    ),
    order: str = Query(
        default=enums.SortedBy.ID,
        description=(
            "Порядок вывода ответа:\n\n"
            f"```{enums.SortedBy.CREATE_DATE.value}``` - по времени создания\n\n"
            f"```{enums.SortedBy.ID.value}``` - по ID товара"
        ),
    ),
    direction: str = Query(
        default=enums.Direction.DESC,
        description=(
            "Порядок сортировки:\n\n"
            f"```{enums.Direction.DESC.value}``` - от большего к меньшему\n\n"
            f"```{enums.Direction.ASC.value}``` - от меньшего к большему"
        ),
    ),
) -> list[dto.Product]:
    """Получить список товаров"""
    return await interactor(
        dto.ProductsQuery(
            limit=limit,
            offset=offset,
            order=order,
            direction=direction,
        ),
    )


def setup() -> APIRouter:
    router = APIRouter(
        prefix="/api/v0/product",
        tags=["Товары"],
        responses={**UNAUTHORIZED_ERROR, **VALIDATION_ERROR}
    )
    router.add_api_route(
        "/count",
        get_all_products,
        methods=[HTTPMethod.GET],
        summary="Список товаров",
        description="Метод возвращает список товаров",
        response_model=list[dto.Product],
        responses={**PRODUCT_LIST},
        response_model_exclude_none=True,
    )
    return router
