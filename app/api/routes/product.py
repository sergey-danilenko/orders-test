from http import HTTPMethod

from dishka.integrations.fastapi import inject, FromDishka
from fastapi import APIRouter

from app.api.dependencies.pagination_sorting import PaginationSortingParams
from app.api.docs.common import (
    UNAUTHORIZED_ERROR, VALIDATION_ERROR
)
from app.api.docs.responses.product import PRODUCT_LIST
from app.core.models import dto
from app.core.services import GetAllProduct


@inject
async def get_all_products(
    interactor: FromDishka[GetAllProduct],
    params: PaginationSortingParams = PaginationSortingParams.as_query(
        limit_entity="товара",
        offset_entity="товара",
    )
) -> list[dto.Product]:
    """Получить список товаров"""
    return await interactor(
        dto.ProductsQuery(
            limit=params.limit,
            offset=params.offset,
            order=params.order,
            direction=params.direction,
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
