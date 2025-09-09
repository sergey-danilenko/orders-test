from enum import Enum


class SortedBy(str, Enum):
    CREATE_DATE = "create_date"
    ID = "id"


class Direction(str, Enum):
    ASC = "asc"
    DESC = "desc"
