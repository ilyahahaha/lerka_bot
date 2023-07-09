from multiprocessing.pool import ThreadPool

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from common.keyboard import ValidCallbacks, get_inline_keyboard
from common.states import MainStateGroup
from schemas.istu import IstuGroup
from schemas.isu import IsuGroup
from services.istu import parse_istu
from services.isu import parse_isu
from settings import Settings
from utils.messages import build_leaderboard, get_default_message

router = Router()

settings = Settings()
SNILS = settings.snils


@router.message(Command(commands=["start"]))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    default_message: str = get_default_message(message.from_user.first_name)
    keyboard = get_inline_keyboard()

    await state.set_state(MainStateGroup.default)

    await message.answer(default_message, reply_markup=keyboard)


@router.callback_query(F.data.startswith("update:"))
async def update_callback_handler(callback: CallbackQuery, state: FSMContext) -> None:
    exact_callback = callback.data
    current_state = await state.get_state()

    pool = ThreadPool(processes=4)
    results = []

    keyboard = get_inline_keyboard()

    if current_state == MainStateGroup.loading:
        return

    await state.set_state(MainStateGroup.loading)

    await callback.message.edit_text("⏱ <b>Обновление данных...</b>")

    match exact_callback:
        case ValidCallbacks.UPDATE_ISU:
            for group in IsuGroup:
                result_coroutine = pool.apply_async(parse_isu, (SNILS, group))

                result = await result_coroutine.get()
                results.append(result)
        case ValidCallbacks.UPDATE_ISTU:
            for group in IstuGroup:
                result_coroutine = pool.apply_async(parse_istu, (SNILS, group))

                result = await result_coroutine.get()
                results.append(result)
        # case ValidCallbacks.UPDATE_BGU:
        #     for group in BguGroup:
        #         result_coroutine = pool.apply_async(parse_bgu, (SNILS, group))

        #         result = await result_coroutine.get()
        #         results.append(result)
        case _:
            await state.set_state(MainStateGroup.error)

            # Log exception
            await callback.message.edit_text(
                "❌ <b>Ошибка!</b> Перезапустите бота.", reply_markup=keyboard
            )

    exact_university = exact_callback.split(":")[1]

    leaderboard = build_leaderboard(results)
    state_data = await state.update_data({exact_university: leaderboard})

    default_message = get_default_message(
        name=callback.from_user.first_name, state_data=state_data
    )

    await state.set_state(MainStateGroup.results)

    await callback.message.edit_text(default_message, reply_markup=keyboard)
