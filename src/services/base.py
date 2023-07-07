from enum import Enum

import orjson
from aiohttp_client_cache import CachedSession, SQLiteBackend
from playwright.async_api import async_playwright


class RequestMethod(Enum):
    GET = 0
    POST = 1


async def get_data(
    url: str,
    payload: dict | None = None,
    method: RequestMethod = RequestMethod.GET,
    parse_response: bool = True,
) -> dict | str:
    async with CachedSession(cache=SQLiteBackend()) as session:
        if method == RequestMethod.POST:
            if payload is None:
                raise ValueError("Невозможно передать пустой запрос")

            response = await session.post(
                url,
                data=orjson.dumps(payload),
                headers={"Content-Type": "application/json"},
            )

            if parse_response:
                response_dict: dict = orjson.loads(await response.text())

                return response_dict

        else:
            response = await session.get(url)

        raw_response = await response.text()
        return raw_response


async def automated_get_data(url: str, selector: str) -> str:
    async with async_playwright() as playwright:
        chromium = playwright.chromium
        browser = await chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("http://bgu.ru/abitur/bach/rating.aspx")
        await page.locator(
            'select[name="ctl00$MainContent$DDLspecList"]'
        ).select_option(value=selector)

        await page.wait_for_load_state("domcontentloaded")

        data = await page.content()

        await browser.close()

        return data
