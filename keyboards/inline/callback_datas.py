"""Описание колбэков"""
from aiogram.utils.callback_data import CallbackData

main_menu_cb = CallbackData(
    "main_menu",
    "level",
    "category",
    "subcategory",
    "action",
    "item_id")


def make_callback_data(
    level,
    category = "0",
    subcategory = "0",
    action = "0",
    item_id = "0"):
    """Формирует callback_data, подставля вместо отсутствующих значений '0'.
    TODO: ValueError: Resulted callback data is too long! из меню менеджер подписок
    """
    return main_menu_cb.new(
        level = level,
        category = category,
        subcategory = subcategory,
        action = action,
        item_id = item_id
    )


sing_item = CallbackData("sing", "user_id", "category", "item_id")
unsing_item = CallbackData("unsing", "user_id","category", "item_id")
