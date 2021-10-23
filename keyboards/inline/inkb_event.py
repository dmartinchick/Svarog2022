from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import callback_data


ink_event_card = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Подписаться", callback_data = "")
        ],
        [
            InlineKeyboardButton(text="Подробнее", callback_data="")
        ]
    ],

)