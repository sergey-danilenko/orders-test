from pathlib import Path
from alembic import op

from app.common.config import Paths, get_paths
from app.common.db_type import DbType

from .run_sql import run_sql_scripts
from .enum_action import DDLAction


def _build_path(target_dir: str = "triggers") -> Path:
    paths: Paths = get_paths()

    match op.get_bind().dialect.name:
        case DbType.POSTGRESQL:
            db_type = DbType.POSTGRESQL
        case _:
            db_type = DbType.SQLITE

    return paths.sql_path / db_type.value / target_dir


def _apply_triggers(action: DDLAction) -> None:
    path = _build_path()
    if path.exists():
        run_sql_scripts(path, action=action)


def create_triggers() -> None:
    _apply_triggers(action=DDLAction.CREATE)


def drop_triggers() -> None:
    _apply_triggers(action=DDLAction.DROP)
