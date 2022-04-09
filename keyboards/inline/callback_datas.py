"""Описание колбэков"""
from aiogram.utils.callback_data import CallbackData

main_menu_cb = CallbackData(
    "main_menu",
    "level",
    "category",
    "subcategory",
    "action",
    "item_id")


admin_panel_cb = CallbackData(
    "ap",
    "to_do",
    "confirmed",
    "event_id"
)


def make_callback_data_mm(
    level,
    category = "0",
    subcategory = "0",
    action = "0",
    item_id = "0"):
    """Формирует callback_data для главного меню,
        подставля вместо отсутствующих значений '0'.
    """
    return main_menu_cb.new(
        level = level,
        category = category,
        subcategory = subcategory,
        action = action,
        item_id = item_id
    )


def make_callback_data_ap(
    to_do = "0",
    confirmed = "0",
    event_id = "0"):
    """Формирует callback_data для панели администратора
    """
    return admin_panel_cb.new(
        to_do = to_do,
        confirmed = confirmed,
        event_id = event_id
    )
