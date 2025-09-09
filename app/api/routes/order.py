from http import HTTPMethod

from dishka.integrations.fastapi import inject, FromDishka
from fastapi import APIRouter, HTTPException, status

from app.api.docs.common import VALIDATION_ERROR
from app.api.docs.responses.order import (
    CREATE_ORDER, UPDATE_ORDER, BAD_REQUEST,
)
from app.core.exception.exception import GatewayError
from app.core.models import dto
from app.core.services import (
    CreateOrder,
    UpdateOrder,
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
        responses={**VALIDATION_ERROR, **BAD_REQUEST}
    )
    router.add_api_route(
        "/create/",
        create_order,
        methods=[HTTPMethod.POST],
        summary="Создать заказ",
        description="Метод создает новый заказ",
        response_model=dto.Order,
        responses={**CREATE_ORDER},
        response_model_exclude_none=True,
    )
    router.add_api_route(
        "/upload/",
        update_order,
        methods=[HTTPMethod.POST],
        summary="Добавить товар в заказ",
        description="Метод добавляет товар в заказ",
        response_model=dto.Order,
        responses={**UPDATE_ORDER},
        response_model_exclude_none=True,
    )

    return router
