from enum import StrEnum

from pydantic import BaseModel


class IstuGroup(StrEnum):
    ECONOMIC = "Экономика"
    ECONOMIC_SECURITY = "Экономическая безопасность"
    URBAN_PLANNING = "Градостроительство"


class IstuCompetitionGroup(BaseModel):
    group: IstuGroup
    place: int

    class Config:
        use_enum_values = True
