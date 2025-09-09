
from pydantic import BaseModel
from fastapi import Depends, Query

from app.core.models import enums


class PaginationSortingParams(BaseModel):
    limit: int
    offset: int
    order: enums.SortedBy
    direction: enums.Direction

    @classmethod
    def as_query(
        cls,
        limit_entity: str = "элементов",
        offset_entity: str = "элемента",
    ):
        def _params(
            limit: int | None = Query(
                default=5,
                description=f"Количество {limit_entity} в ответе",
            ),
            offset: int | None = Query(
                default=0,
                description=f"Смещение относительно первого {offset_entity}"),
            order: enums.SortedBy = Query(
                default=enums.SortedBy.ID,
                description=(
                    "Порядок вывода ответа:\n\n"
                    f"```{enums.SortedBy.CREATE_DATE.value}``` - по времени создания\n\n"
                    f"```{enums.SortedBy.ID.value}``` - по ID {offset_entity}"
                ),
            ),
            direction: enums.Direction = Query(
                default=enums.Direction.DESC,
                description=(
                    "Порядок сортировки:\n\n"
                    f"```{enums.Direction.DESC.value}``` - от большего к меньшему\n\n"
                    f"```{enums.Direction.ASC.value}``` - от меньшего к большему"
                ),
            ),
        ) -> "PaginationSortingParams":
            return cls(limit=limit, offset=offset, order=order, direction=direction)
        return Depends(_params)