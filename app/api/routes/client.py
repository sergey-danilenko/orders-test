from http import HTTPMethod

from dishka.integrations.fastapi import inject, FromDishka
from fastapi import APIRouter

from app.api.dependencies.pagination_sorting import PaginationSortingParams
from app.api.docs.common import (
    UNAUTHORIZED_ERROR, VALIDATION_ERROR
)
from app.api.docs.responses.client import CLIENT_LIST
from app.core.models import dto
from app.core.services import GetAllClients


@inject
async def get_all_clients(
    interactor: FromDishka[GetAllClients],
    params: PaginationSortingParams = PaginationSortingParams.as_query(
        limit_entity="клиентов",
        offset_entity="клиента",
    )
) -> list[dto.Client]:
    """Получить список клиентов"""
    return await interactor(
        dto.ClientsQuery(
            limit=params.limit,
            offset=params.offset,
            order=params.order,
            direction=params.direction,
        ),
    )


def setup() -> APIRouter:
    router = APIRouter(
        prefix="/api/v0/client",
        tags=["Клиенты"],
        responses={**UNAUTHORIZED_ERROR, **VALIDATION_ERROR}
    )
    router.add_api_route(
        "/count",
        get_all_clients,
        methods=[HTTPMethod.GET],
        summary="Список клиентов",
        description="Метод возвращает список клиентов",
        response_model=list[dto.Client],
        responses={**CLIENT_LIST},
        response_model_exclude_none=True,
    )
    return router
