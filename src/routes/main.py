from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from schemas.bgu import BguGroup
from services.bgu import parse_bgu
from settings import Settings

router = Router()

settings = Settings()

SNILS = settings.snils


@router.message(Command(commands=["start"]))
async def command_start_handler(message: Message) -> None:
    for group in BguGroup:
        group = await parse_bgu(SNILS, group=group)

        await message.answer(str(group))
