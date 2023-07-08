from multiprocessing.pool import ThreadPool

from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from common.keyboard import get_inline_keyboard
from common.states import MainStateGroup
from schemas.istu import IstuCompetitionGroup, IstuGroup
from schemas.isu import IsuCompetitionGroup, IsuGroup
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


@router.callback_query(Text("update_istu"))
async def refresh_istu_state_handler(
    callback: CallbackQuery, state: FSMContext
) -> None:
    keyboard = get_inline_keyboard()

    current_state = await state.get_state()
    if current_state == MainStateGroup.loading:
        return

    await state.set_state(MainStateGroup.loading)

    await callback.message.edit_text("⏱ <b>Обновление данных...</b>")

    pool = ThreadPool(processes=len(IstuGroup))
    results: list[IstuCompetitionGroup] = []

    for group in IstuGroup:
        async_result = pool.apply_async(parse_istu, (SNILS, group))

        try:
            result = await async_result.get()
        except Exception:
            await state.set_state(MainStateGroup.results)
            data = await state.update_data({"istu_leaderboard": None})

            default_message = get_default_message(
                callback.from_user.first_name,
                isu_leaderboard=data.get("isu_leaderboard"),
                istu_leaderboard=data.get("istu_leaderboard"),
                bgu_leaderboard=data.get("bgu_leaderboard"),
            )

            return await callback.message.edit_text(
                default_message, reply_markup=keyboard
            )

        results.append(result)

    await state.set_state(MainStateGroup.results)
    leaderboard = build_leaderboard(results)
    data = await state.update_data({"istu_leaderboard": leaderboard})

    default_message = get_default_message(
        callback.from_user.first_name,
        isu_leaderboard=data.get("isu_leaderboard"),
        istu_leaderboard=data.get("istu_leaderboard"),
        bgu_leaderboard=data.get("bgu_leaderboard"),
    )

    await callback.message.edit_text(default_message, reply_markup=keyboard)


@router.callback_query(Text("update_isu"))
async def refresh_isu_state_handler(callback: CallbackQuery, state: FSMContext) -> None:
    keyboard = get_inline_keyboard()

    current_state = await state.get_state()
    if current_state == MainStateGroup.loading:
        return

    await state.set_state(MainStateGroup.loading)

    await callback.message.edit_text("⏱ <b>Обновление данных...</b>")

    pool = ThreadPool(processes=len(IsuGroup))
    results: list[IsuCompetitionGroup] = []

    for group in IsuGroup:
        async_result = pool.apply_async(parse_isu, (SNILS, group))

        try:
            result = await async_result.get()
        except Exception:
            await state.set_state(MainStateGroup.results)
            data = await state.update_data({"isu_leaderboard": None})

            default_message = get_default_message(
                callback.from_user.first_name,
                isu_leaderboard=data.get("isu_leaderboard"),
                istu_leaderboard=data.get("istu_leaderboard"),
                bgu_leaderboard=data.get("bgu_leaderboard"),
            )

            return await callback.message.edit_text(
                default_message, reply_markup=keyboard
            )

        results.append(result)

    await state.set_state(MainStateGroup.results)
    leaderboard = build_leaderboard(results)
    data = await state.update_data({"isu_leaderboard": leaderboard})

    default_message = get_default_message(
        callback.from_user.first_name,
        isu_leaderboard=data.get("isu_leaderboard"),
        istu_leaderboard=data.get("istu_leaderboard"),
        bgu_leaderboard=data.get("bgu_leaderboard"),
    )

    await callback.message.edit_text(default_message, reply_markup=keyboard)
