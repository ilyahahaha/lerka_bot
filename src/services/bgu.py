from bs4 import BeautifulSoup, PageElement, ResultSet

from schemas.bgu import BguCompetitionGroup, BguGroup
from services.base import automated_get_data
from utils.snils import format_snils


async def parse_bgu(
    snils: str, group: BguGroup = BguGroup.ECONOMIC
) -> BguCompetitionGroup:
    match group:
        case BguGroup.STAFF_MANAGEMENT:
            value_to_select = "38.03.03 Управление персоналом"
        case BguGroup.BUSINESS_INFORMATICS:
            value_to_select = "38.03.05 Бизнес-информатика"
        case BguGroup.ECONOMIC:
            value_to_select = "38.03.01 Экономика"
        case _:
            raise ValueError("Неверное значение конкурсной группы")

    try:
        data = await automated_get_data(
            url="http://bgu.ru/abitur/bach/rating.aspx", selector=value_to_select
        )
    except Exception:
        raise Exception("Ошибка при получении данных БГУ.")
    else:
        if data is None:
            raise Exception("Ошибка при получении данных БГУ.")

    soup = BeautifulSoup(data, "lxml")

    rating_table = soup.find("table")
    rating_data: ResultSet[PageElement] = rating_table.find_all("tr")[2:]

    lerka_data: list[PageElement] = [
        tr
        for tr in rating_data
        if tr.find_next("td").contents[0].text.strip() == format_snils(snils)
    ]

    group_object = BguCompetitionGroup(
        group=group,
        place=int(lerka_data[0].find_all_next("td")[1].text.strip()),
    )

    return group_object
