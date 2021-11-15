"""Создание клавиатуры панели администратора"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import make_callback_data_ap

async def admin_panel_keyboard() -> InlineKeyboardMarkup:
    """Возвращает пользователю меню панели администратора

    Returns:
        InlineKeyboardMarkup: Клавиатура со списком категорий
    """
    markup = InlineKeyboardMarkup(
        row_width=1
    )
    categories = [
        {'name':"📝 Добавление результатов", 'category_item':"add_result"},
        {'name':"✏ Изменение результатов", 'category_item':"change_result"},
        {'name':"🕑 Изменение расписания", 'category_item':"changing_shedule"},
        {'name':"⚡ Экстренное сообщение", 'category_item':"emergency_message"}
    ]

    for category in categories:
        markup.insert(
            InlineKeyboardButton(
                text=category['name'],
                callback_data=make_callback_data_ap(category['category_item'])
            )
        )
    return markup
