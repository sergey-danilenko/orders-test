import logging

from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    async_sessionmaker, create_async_engine, AsyncEngine, AsyncSession,
)
from sqlalchemy.engine import make_url

from app.common.config import DbConfig
from app.common.db_type import DbType

logger = logging.getLogger(__name__)


def create_alembic_url(
    db_config: DbConfig,
    async_fallback: bool = False,
) -> str:
    uri = db_config.uri
    if db_config.type == DbType.POSTGRESQL:
        if async_fallback:
            uri += "?async_fallback=True"
    elif db_config.type == DbType.SQLITE:
        uri = f"{db_config.type}:///{db_config.dbname}"
    return uri


def create_engine(db_config: DbConfig, echo: bool = False) -> AsyncEngine:
    url = make_url(db_config.uri)
    logger.info("Sqlalchemy URL: %s", url)
    engine = create_async_engine(
        url=url,
        echo=echo if echo else db_config.echo,
        pool_pre_ping=db_config.pool_pre_ping,
    )

    if db_config.type == DbType.SQLITE:
        @event.listens_for(engine.sync_engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON;")
            cursor.close()
    return engine


def create_session_maker(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    pool: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=engine, expire_on_commit=False, future=True, autoflush=False
    )
    return pool
