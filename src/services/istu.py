from bs4 import BeautifulSoup

from schemas.istu import IstuCompetitionGroup, IstuGroup
from services.base import get_data


async def parse_istu(
    snils: str, group: IstuGroup = IstuGroup.ECONOMIC
) -> IstuCompetitionGroup:
    match group:
        case IstuGroup.ECONOMIC:
            url = f"https://www.istu.edu/served/rating.php?n={24356}"
        case IstuGroup.ECONOMIC_SECURITY:
            url = f"https://www.istu.edu/served/rating.php?n={24354}"
        case IstuGroup.URBAN_PLANNING:
            url = f"https://www.istu.edu/served/rating.php?n={24199}"
        case _:
            raise ValueError("Неверное значение конкурсной группы")

    try:
        data = await get_data(url=url)
    except Exception:
        raise Exception("Ошибка при получении данных ИРНИТУ.")
    else:
        if data is None:
            raise Exception("Ошибка при получении данных ИРНИТУ.")

    soup = BeautifulSoup(data, "lxml")

    rating_table = soup.find("table")
    lerka_data = rating_table.find(attrs={"data-filter": f'["{snils}"]'})

    if lerka_data is None:
        raise Exception("Ошибка при получении данных ИРНИТУ.")

    group_object = IstuCompetitionGroup(
        group=group, place=int([el.text for el in lerka_data.find_all("td")][0])
    )

    return group_object
