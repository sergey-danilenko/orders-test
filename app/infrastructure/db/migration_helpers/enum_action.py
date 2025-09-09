from enum import Enum


class DDLAction(str, Enum):
    CREATE = "create"
    DROP = "drop"
