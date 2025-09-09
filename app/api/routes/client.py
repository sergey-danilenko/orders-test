from http import HTTPMethod

from dishka.integrations.fastapi import inject, FromDishka
from fastapi import APIRouter, Query

from app.api.docs.common import (
    UNAUTHORIZED_ERROR, VALIDATION_ERROR
)
from app.api.docs.responses.client import CLIENT_LIST
from app.core.models import dto, enums
from app.core.services import GetAllClients


@inject
async def get_all_clients(
    interactor: FromDishka[GetAllClients],
    limit: int = Query(default=5, description="Количество клиентов в ответе"),
    offset: int = Query(
        default=0,
        description="Смещение относительно первого клиента",
    ),
    order: str = Query(
        default=enums.SortedBy.ID,
        description=(
            "Порядок вывода ответа:\n\n"
            f"```{enums.SortedBy.CREATE_DATE.value}``` - по времени создания\n\n"
            f"```{enums.SortedBy.ID.value}``` - по ID клиента"
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
) -> list[dto.Client]:
    """Получить список клиентов"""
    return await interactor(
        dto.ClientsQuery(
            limit=limit,
            offset=offset,
            order=order,
            direction=direction,
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
