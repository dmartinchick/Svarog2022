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
    "what_to_do"
)

ap_add_result_cb = CallbackData(
    "ap_add_result",
    "event_id",
    "team_id",
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
    what_to_do = "0"):
    """Формирует callback_data для панели администратора
    """
    return admin_panel_cb.new(
        what_to_do = what_to_do
    )


def make_callback_data_app_add_result(
    event_id = "0",
    team_id = "0"):
    """Формирует callback_data для меню добавления результатотв"""
    return ap_add_result_cb.new(
        event_id = event_id,
        team_id = team_id
    )
