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
    "event_id"
)

ap_add_result_cb = CallbackData(
    "ap_add_result",
    "event_id",
    "to_do"
)

ap_clear_reslt_cb = CallbackData(
    "ap_clear_result",
    "event_id",
    "to_do"
)


ap_events_cb = CallbackData(
    "ap_events",
    "to_do",
    "event_id",
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
    to_do = "0",
    event_id = "0"):
    """Формирует callback_data для панели администратора
    """
    return admin_panel_cb.new(
        to_do = to_do,
        event_id = event_id
    )


def make_callback_data_ap_events(
    to_do = "0",
    event_id = "0") -> CallbackData:
    """Формирует callback_data для меню с конкурсами

    Args:
        event_id (str, optional): id конкурса. Defaults to "0".
        to_do (str, optional): что нужно сделать с конкурсом. Defaults to "0".

    Returns:
        CallbackData: callback_data
    """
    return ap_events_cb.new(
        to_do = to_do,
        event_id = event_id,
    )
