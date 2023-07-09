from enum import StrEnum

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class ValidCallbacks(StrEnum):
    UPDATE_ISU = "update:isu"
    UPDATE_ISTU = "update:istu"
    UPDATE_BGU = "update:bgu"


def get_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        *[
            InlineKeyboardButton(
                text="1️⃣ Обновить ИГУ", callback_data=ValidCallbacks.UPDATE_ISU
            ),
            InlineKeyboardButton(
                text="2️⃣ Обновить ИРНИТУ", callback_data=ValidCallbacks.UPDATE_ISTU
            ),
        ]
    )

    # builder.row(
    #     *[
    #         InlineKeyboardButton(
    #             text="3️⃣ Обновить БГУ", callback_data=ValidCallbacks.UPDATE_BGU
    #         )
    #     ]
    # )

    return builder.as_markup()
