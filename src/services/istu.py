import asyncio
import logging

from aiohttp_client_cache import CachedSession, SQLiteBackend
from bs4 import BeautifulSoup
from schemas.istu import IstuCompetitionGroup, IstuGroup
from settings import Settings

settings = Settings()


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
            async with session.get(url, timeout=settings.request_timeout) as response:
                data = await response.text()
    except asyncio.TimeoutError:
        logging.error(f"ISTU [{group}] - request timeout")
        return None

    if data is None:
        logging.error(f"ISTU [{group}] - request data null")
        return None

    soup = BeautifulSoup(data, "lxml")

    rating_table = soup.find("table")
    lerka_data = rating_table.find(attrs={"data-filter": f'["{snils}"]'})

    if lerka_data is None:
        logging.error(f"ISTU [{group}] - parsed data null")
        return None

    group_object = IstuCompetitionGroup(
        group=group, place=int([el.text for el in lerka_data.find_all("td")][0])
    )

    return group_object
