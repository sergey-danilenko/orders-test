from typing import TypeVar, Generic, Sequence, Callable

from sqlalchemy import select, ScalarResult, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import ORMOption

from sqlalchemy.dialects.sqlite import (
    insert as sqlite_insert,
    Insert as Insert_sqlite
)
from sqlalchemy.dialects.postgresql import (
    insert as pg_insert,
    Insert as Insert_pg,
)

from app.common.db_type import DbType
from app.core.models import dto, enums
from app.infrastructure.db.models import Base

Model_co = TypeVar("Model_co", bound=Base, covariant=True, contravariant=False)

InsertVariant = Callable[[type[Base]], Insert_sqlite | Insert_pg]


def _setup_insert(dialect: str) -> InsertVariant:
    match dialect:
        case DbType.POSTGRESQL:
            return pg_insert
        case _:
            return sqlite_insert


class BaseDbGateway(Generic[Model_co]):
    def __init__(
        self,
        model: type[Model_co],
        session: AsyncSession,
    ):
        self.model = model
        self.session = session
        self.dialect: str = self.session.bind.dialect.name
        self._insert: InsertVariant = _setup_insert(self.dialect)

    @property
    def insert(self) -> InsertVariant:
        return self._insert

    async def _get_by_id(
        self, id_: int, options: Sequence[ORMOption] = None,
    ) -> Model_co:
        result = await self.session.get(
            self.model, id_, options=options,
        )
        return result

    async def _get_all(
        self,
        options: Sequence[ORMOption] = None,
        query: dto.BaseQuery = None,
    ) -> Sequence[Model_co]:
        stmt = select(self.model)
        if options:
            stmt = stmt.options(*options)
        if query is not None:
            stmt = (
                self._apply_sorting(
                    stmt=stmt,
                    order=query.order,
                    direction=query.direction,
                )
                .limit(query.limit)
                .offset(query.offset)
            )

        result: ScalarResult[Model_co] = await self.session.scalars(stmt)
        return result.all()

    def _add(self, obj: Base):
        self.session.add(obj)

    def _add_all(self, *objects: Base):
        self.session.add_all(objects)

    async def commit(self):
        await self.session.commit()

    async def _flush(self, *objects: Base):
        await self.session.flush(objects)

    def _apply_sorting(
        self,
        stmt: Select,
        model: type[Model_co] | None = None,
        order: str = enums.SortedBy.ID,
        direction: str = enums.Direction.DESC,
    ) -> Select:
        if not model:
            model = self.model

        sort_by = getattr(model, order, None)
        if sort_by is None:
            sort_by = getattr(model, enums.SortedBy.ID)

        if direction.lower() == enums.Direction.DESC:
            return stmt.order_by(sort_by.desc())
        else:
            return stmt.order_by(sort_by.asc())
