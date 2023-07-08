from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        *[
            InlineKeyboardButton(text="1️⃣ Обновить ИГУ", callback_data="update_isu"),
            InlineKeyboardButton(
                text="2️⃣ Обновить ИРНИТУ", callback_data="update_istu"
            ),
        ]
    )

    builder.row(
        *[InlineKeyboardButton(text="3️⃣ Обновить БГУ", callback_data="update_bgu")]
    )

    return builder.as_markup()
