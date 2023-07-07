from enum import StrEnum

from pydantic import BaseModel


class BguGroup(StrEnum):
    STAFF_MANAGEMENT = "Управление персоналом"  # 38.03.03 Управление персоналом
    BUSINESS_INFORMATICS = "Бизнес-информатика" # 38.03.05 Бизнес-информатика
    ECONOMIC = "Экономика" # 38.03.01 Экономика


class BguCompetitionGroup(BaseModel):
    group: BguGroup
    place: int

    class Config:
        use_enum_values = True
