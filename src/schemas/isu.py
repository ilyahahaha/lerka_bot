from enum import StrEnum

from pydantic import BaseModel


class IsuGroup(StrEnum):
    LANG_LITERATURE = "Русский язык - Литература"
    HISTORY_SOCIAL = "История - Обществознание"
    PRIMARY_ADDITIONAL_EDUCATION = "Начальное образование - Дополнительное образование"


class IsuCompetitionGroup(BaseModel):
    group: IsuGroup
    place: int

    class Config:
        use_enum_values = True
