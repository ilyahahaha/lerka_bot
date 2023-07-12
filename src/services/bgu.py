import asyncio
import logging

from aiohttp import ClientSession
from bs4 import BeautifulSoup, PageElement, ResultSet
from schemas.bgu import BguCompetitionGroup, BguGroup
from settings import Settings
from utils.snils import format_snils

settings = Settings()


async def parse_bgu(
    snils: str, group: BguGroup = BguGroup.ECONOMIC
) -> BguCompetitionGroup | None:
    url = "http://bgu.ru/abitur/bach/rating.aspx"

    match group:
        case BguGroup.STAFF_MANAGEMENT:
            spec_list = '13298#6# "Управление персоналом"'
        case BguGroup.BUSINESS_INFORMATICS:
            spec_list = '13302#4# "Цифровая экономика"'
        case BguGroup.ECONOMIC:
            spec_list = '13294#46# "Внешнеэкономическая деятельность";  "Финансы и кредит";  "Экономика нефтегазового комплекса";  "Экономика предприятия и предпринимательская деятельность";  "Мировая экономика (Русско-китайская программа двойного дипломирования г. Пекин)"'
        case _:
            raise ValueError("Неверное значение конкурсной группы")

    try:
        async with ClientSession() as session:
            initial_response = await session.get(url, timeout=settings.request_timeout)
            initial_data = await initial_response.text()
            initial_soup = BeautifulSoup(initial_data, "lxml")

            view_state = initial_soup.select_one("#__VIEWSTATE")["value"]
            event_validation = initial_soup.select_one("#__EVENTVALIDATION")["value"]

            form_data = {
                "__EVENTTARGET": "ctl00$MainContent$DDLspecList",
                "__EVENTARGUMENT": "",
                "__LASTFOCUS": "",
                "__VIEWSTATE": view_state,
                "__EVENTVALIDATION": event_validation,
                "ctl00$MainContent$DDLedu": 3,
                "ctl00$MainContent$DDLtypeKonkurs": 1,
                "ctl00$MainContent$DDLformStudy": 1,
                "ctl00$MainContent$DDLspecList": spec_list,
            }

            data_response = await session.post(url, data=form_data)

            final_data = await data_response.text()
            soup = BeautifulSoup(final_data, "lxml")

            rating_table = soup.find("table")
            rating_data: ResultSet[PageElement] = rating_table.find_all("tr")[2:]

            lerka_data: list[PageElement] = [
                tr
                for tr in rating_data
                if tr.find_next("td").contents[0].text.strip() == format_snils(snils)
            ]

            if len(lerka_data) == 0:
                logging.error(f"BGU [{group}] - parsed data is null")
                return None

            group_object = BguCompetitionGroup(
                group=group,
                place=int(lerka_data[0].find_all_next("td")[1].text.strip()),
            )

            return group_object
    except asyncio.TimeoutError:
        logging.error(f"BGU [{group}] - request timeout")
        return None
