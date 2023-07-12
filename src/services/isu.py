import asyncio
import logging

import orjson
from aiohttp_client_cache import CachedSession, SQLiteBackend
from schemas.isu import IsuCompetitionGroup, IsuGroup
from settings import Settings
from utils.snils import format_snils

settings = Settings()


async def parse_isu(
    snils: str, group: IsuGroup = IsuGroup.LANG_LITERATURE
) -> IsuCompetitionGroup | None:
    request_data = {
        "processor": "rating_getListAbiturients",
        "КонкурснаяГруппа": {
            "type": "CatalogRef",
            "catalog": "КонкурсныеГруппы",
            "uid": "uid",
            "name": "44.03.05 Педагогическое образование (с двумя профилями подготовки) Очная Бюджетная основа",  # noqa: E501
        },
    }

    match group:
        case IsuGroup.LANG_LITERATURE:
            request_data["КонкурснаяГруппа"][
                "uid"
            ] = "ec7428e7-ca32-11ed-8105-82761dd90eed"
        case IsuGroup.HISTORY_SOCIAL:
            request_data["КонкурснаяГруппа"][
                "uid"
            ] = "ec7428e2-ca32-11ed-8105-82761dd90eed"
        case IsuGroup.PRIMARY_ADDITIONAL_EDUCATION:
            request_data["КонкурснаяГруппа"][
                "uid"
            ] = "e65356ff-ca32-11ed-8105-82761dd90eed"
            request_data["КонкурснаяГруппа"][
                "name"
            ] = "44.03.05 Педагогическое образование (с двумя профилями подготовки) Очная Бюджетная основа"  # noqa: E501
        case _:
            raise ValueError("Неверное значение конкурсной группы")

    try:
        async with CachedSession(cache=SQLiteBackend()) as session:
            async with session.post(
                "https://pk.isu.ru/x/getProcessor",
                data=orjson.dumps(request_data),
                headers={"Content-Type": "application/json"},
                timeout=settings.request_timeout,
            ) as response:
                data_dict: dict = orjson.loads(await response.text())
    except asyncio.TimeoutError:
        logging.error(f"ISU [{group}] - request timeout")
        return None
    except orjson.JSONDecodeError:
        logging.error(f"ISU [{group}] - missed json")
        return None

    if "data" not in data_dict:
        logging.error(f"ISU [{group}] - json data null")
        return None

    lerka_data: list[dict] = list(
        filter(
            lambda person: person["СНИЛС"] == format_snils(snils),
            data_dict["data"],
        )
    )

    if len(lerka_data) == 0:
        logging.error(f"ISU [{group}] - parse json data null")
        return None

    group_object = IsuCompetitionGroup(group=group, place=lerka_data[0].get("Место"))

    return group_object
