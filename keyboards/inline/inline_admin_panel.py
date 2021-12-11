"""Создание клавиатуры панели администратора"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import make_callback_data_ap, make_callback_data_app_add_result
from utils.db_api.db_comands import get_events_list

async def admin_panel_keyboard() -> InlineKeyboardMarkup:
    """Возвращает пользователю меню панели администратора

    Returns:
        InlineKeyboardMarkup: Клавиатура со списком категорий
    """
    markup = InlineKeyboardMarkup(
        row_width=1
    )
    to_do_list = [
        {'name':"📝 Добавление результатов", 'what_to_do_item':"add_result"},
        {'name': "Очиститть результаты конкруса", 'what_to_do_item':"claer_result"},
        {'name':"✏ Изменение результатов команды", 'what_to_do_item':"change_result"},
        {'name':"Добавить штраф", 'what_to_do_item':"set_fol"},
        {'name':"🕑 Изменение расписания", 'what_to_do_item':"changing_shedule"},
        {'name':"⚡ Экстренное сообщение", 'what_to_do_item':"emergency_message"}
    ]

    for to_do in to_do_list:
        markup.insert(
            InlineKeyboardButton(
                text=to_do['name'],
                callback_data=make_callback_data_ap(
                    what_to_do=to_do['what_to_do_item'])
            )
        )
    return markup

async def ap_event_keyboard() -> InlineKeyboardMarkup:
    """Возвращает пользователю клавиатуру событий

    Returns:
        InlineKeyboardMarkup: Клавиатура событий
    """
    markup = InlineKeyboardMarkup(
        row_width=1
    )
    events = get_events_list()
    for event in events:
        markup.insert(
            InlineKeyboardButton(
                text=event['name'],
                callback_data=make_callback_data_app_add_result(
                    item_id = event['item_id']
                )
            )
        )
    return markup
