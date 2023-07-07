from schemas.isu import IsuCompetitionGroup, IsuGroup
from services.base import RequestMethod, get_data
from settings import Settings
from utils.snils import format_snils

settings = Settings()


async def parse_isu(
    snils: str, group: IsuGroup = IsuGroup.LANG_LITERATURE
) -> IsuCompetitionGroup:
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
        data_dict = await get_data(
            url="https://pk.isu.ru/x/getProcessor",
            payload=request_data,
            method=RequestMethod.POST,
        )
    except Exception:
        raise Exception("Ошибка при получении данных ИГУ.")
    else:
        if "data" not in data_dict:
            raise Exception("Ошибка при получении данных ИГУ.")

    lerka_data: list[dict] = list(
        filter(
            lambda person: person["СНИЛС"] == format_snils(snils),
            data_dict["data"],
        )
    )

    if len(lerka_data) == 0:
        raise Exception("Ошибка при расшифровке данных ИГУ.")

    group_object = IsuCompetitionGroup(group=group, place=lerka_data[0].get("Место"))

    return group_object
