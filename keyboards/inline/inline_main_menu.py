from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import main_menu_choice

inkb_main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Что сейчас происходит", callback_data=main_menu_choice.new(
                item_name="what_now"
            )),
        ],
        [
            InlineKeyboardButton(text="Ближайшие мероприятия",callback_data="main:what_next"),
        ],
        [
            InlineKeyboardButton(text="Полное расписание",callback_data="main:full_schedule"),
        ],
        [
            InlineKeyboardButton(text="Результаты", callback_data="main:results"),
        ],
        [
            InlineKeyboardButton(text="Конкурсы", callback_data="main:contests"),
        ],
        [
            InlineKeyboardButton(text="Команды", callback_data="main:team"),
        ],
        [
            InlineKeyboardButton(text="Менеджер подписок", callback_data="main:subscriptions_manager"),
        ],
        [
            InlineKeyboardButton(text="Карта фестиваля", callback_data="main:map"),
        ],
        [
            InlineKeyboardButton(text="Поделиться ссылкой", callback_data="main:share"),
        ],
        [
            InlineKeyboardButton(text="Положения фестиваля", callback_data="main:about")
        ]
    ]
)
