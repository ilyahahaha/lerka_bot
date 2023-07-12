from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from common.keyboard import ValidCallbacks, get_inline_keyboard
from common.states import MainStateGroup
from schemas.bgu import BguGroup
from schemas.istu import IstuGroup
from schemas.isu import IsuGroup
from services.bgu import parse_bgu
from services.istu import parse_istu
from services.isu import parse_isu
from settings import Settings
from utils.messages import build_leaderboard, get_default_message

router = Router()

settings = Settings()
SNILS = settings.snils


@router.message(Command(commands=["start"]))
async def command_start_handler(message: Message) -> None:
    if message.from_user.id not in settings.allowed_ids:
        return await message.answer("❌ <b>Вам запрещено пользоваться этим ботом!</b>")

    default_message: str = get_default_message(message.from_user.first_name)
    keyboard = get_inline_keyboard()

    await message.answer(default_message, reply_markup=keyboard)


@router.callback_query(F.data.startswith("update:"))
async def update_callback_handler(callback: CallbackQuery, state: FSMContext) -> None:
    parse_results = []

    exact_callback = callback.data
    keyboard = get_inline_keyboard()

    await state.set_state(MainStateGroup.loading)
    await callback.message.edit_text("⏱ <b>Обновление данных...</b>")

    match exact_callback:
        case ValidCallbacks.UPDATE_ISU:
            for group in IsuGroup:
                isu_result = await parse_isu(snils=SNILS, group=group)

                parse_results.append(isu_result)
        case ValidCallbacks.UPDATE_ISTU:
            for group in IstuGroup:
                istu_result = await parse_istu(snils=SNILS, group=group)

                parse_results.append(istu_result)
        case ValidCallbacks.UPDATE_BGU:
            for group in BguGroup:
                bgu_result = await parse_bgu(snils=SNILS, group=group)

                parse_results.append(bgu_result)
        case _:
            await state.set_state(MainStateGroup.error)

            await callback.message.edit_text(
                "❌ <b>Ошибка!</b> Перезапустите бота.", reply_markup=keyboard
            )

    await state.set_state(MainStateGroup.results)

    leaderboard = build_leaderboard(parse_results)
    state_data = await state.update_data({exact_callback: leaderboard})

    default_message = get_default_message(
        name=callback.from_user.first_name, state_data=state_data
    )

    await callback.message.edit_text(default_message, reply_markup=keyboard)
