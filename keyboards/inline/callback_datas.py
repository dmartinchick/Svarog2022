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
    "admin_panel",
    "category"
)


def make_callback_data(
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
    category):
    """Формирует callback_data для панели администратора
    """
    return admin_panel_cb.new(
        category = category
    )
