import logging
from pathlib import Path
from alembic import op

from sqlalchemy.exc import OperationalError, ProgrammingError

from .enum_action import DDLAction

logger = logging.getLogger(__name__)


def run_sql_scripts(
    path: Path,
    action: DDLAction = DDLAction.CREATE,  # "create" | "drop"
    extension: str = "sql",
) -> None:
    pattern = f"{action.value}_*.{extension}"
    for file in sorted(path.glob(pattern)):
        sql = file.read_text(encoding="utf-8")
        if sql:
            try:
                op.execute(sql)
            except (OperationalError, ProgrammingError) as e:
                logging.warning(f"Failed to execute {file.name}: {e}")
