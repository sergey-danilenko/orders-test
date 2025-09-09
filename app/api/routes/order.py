from http import HTTPMethod

from dishka.integrations.fastapi import inject, FromDishka
from fastapi import APIRouter, HTTPException, status

from app.api.dependencies.pagination_sorting import PaginationSortingParams
from app.api.docs.common import (
    UNAUTHORIZED_ERROR, VALIDATION_ERROR
)
from app.api.docs.responses.order import (
    ORDERS_LIST, CREATE_ORDER, UPDATE_ORDER, BAD_REQUEST,
)
from app.core.exception.exception import GatewayError
from app.core.models import dto
from app.core.services import (
    GetAllOrders,
    CreateOrder,
    UpdateOrder,
)


@inject
async def get_all_orders(
    interactor: FromDishka[GetAllOrders],
    params: PaginationSortingParams = PaginationSortingParams.as_query(
        limit_entity="заказов",
        offset_entity="заказа",
    )
) -> list[dto.Order]:
    """Получить список заказов"""
    return await interactor(
        dto.OrdersQuery(
            limit=params.limit,
            offset=params.offset,
            order=params.order,
            direction=params.direction,
        ),
    )


@inject
async def create_order(
    new_order: dto.CreateOrder,
    interactor: FromDishka[CreateOrder],
) -> dto.Order:
    """Создать заказ"""
    try:
        return await interactor(new_order)
    except GatewayError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.notify_info,
        )


@inject
async def update_order(
    upload_order: dto.UpdateOrder,
    interactor: FromDishka[UpdateOrder],
) -> dto.Order:
    """Обновить заказ"""
    try:
        return await interactor(upload_order)
    except GatewayError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.notify_info,
        )


def setup() -> APIRouter:
    router = APIRouter(
        prefix="/api/v0/order",
        tags=["Заказы"],
        responses={**UNAUTHORIZED_ERROR, **VALIDATION_ERROR}
    )
    router.add_api_route(
        "/count/",
        get_all_orders,
        methods=[HTTPMethod.GET],
        summary="Список Заказов",
        description="Метод возвращает список заказов",
        response_model=list[dto.Order],
        responses={**ORDERS_LIST},
        response_model_exclude_none=True,
    )
    router.add_api_route(
        "/create/",
        create_order,
        methods=[HTTPMethod.POST],
        summary="Создать заказ",
        description="Метод создает новый заказ",
        response_model=dto.Order,
        responses={**CREATE_ORDER, **BAD_REQUEST},
        response_model_exclude_none=True,
    )
    router.add_api_route(
        "/upload/",
        update_order,
        methods=[HTTPMethod.POST],
        summary="Добавить товар в заказ",
        description="Метод добавляет товар в заказ",
        response_model=dto.Order,
        responses={**UPDATE_ORDER, **BAD_REQUEST},
        response_model_exclude_none=True,
    )

    return router
