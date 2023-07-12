import asyncio
import logging

from aiogram import Bot, Dispatcher
from routes.main import router as main_router
from settings import Settings

settings = Settings()


async def main() -> None:
    dp = Dispatcher()
    dp.include_router(main_router)

    bot = Bot(settings.bot_token, parse_mode="HTML")
    await dp.start_polling(bot, skip_updates=False)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
