from aiohttp_client_cache import CachedSession, SQLiteBackend
from bs4 import BeautifulSoup
from schemas.istu import IstuCompetitionGroup, IstuGroup


async def parse_istu(
    snils: str, group: IstuGroup = IstuGroup.ECONOMIC
) -> IstuCompetitionGroup | None:
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
        async with CachedSession(cache=SQLiteBackend()) as session:
            async with session.get(url) as response:
                data = await response.text()
    except Exception:
        # TODO: log exception
        return None
    else:
        # TODO: log that data is None
        if data is None:
            return None

    soup = BeautifulSoup(data, "lxml")

    rating_table = soup.find("table")
    lerka_data = rating_table.find(attrs={"data-filter": f'["{snils}"]'})

    if lerka_data is None:
        return None

    group_object = IstuCompetitionGroup(
        group=group, place=int([el.text for el in lerka_data.find_all("td")][0])
    )

    return group_object
