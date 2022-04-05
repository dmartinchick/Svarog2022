"""Создание клавиатуры панели администратора"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import make_callback_data_ap, make_callback_data_ap_events

async def admin_panel_keyboard() -> InlineKeyboardMarkup:
    """Возвращает пользователю меню панели администратора

    Returns:
        InlineKeyboardMarkup: Клавиатура со списком категорий
    """
    markup = InlineKeyboardMarkup(
        row_width=1
    )
    to_do_list = [
        {'name':"📝 Добавление результатов", 'to_do_item':"add_result"},
        {'name': "Очиститть результаты конкруса", 'to_do_item':"claer_result"},
        {'name':"✏ Изменение результатов команды", 'to_do_item':"change_result"},
        {'name':"Добавить штраф", 'to_do_item':"set_fol"},
        {'name':"🕑 Изменение расписания", 'to_do_item':"changing_shedule"},
        {'name':"⚡ Экстренное сообщение", 'to_do_item':"emergency_message"}
    ]

    for to_do in to_do_list:
        markup.insert(
            InlineKeyboardButton(
                text=to_do['name'],
                callback_data=make_callback_data_ap(
                    to_do=to_do['to_do_item'])
            )
        )
    return markup

async def ap_event_keyboard(
    events_list:list,
    results_list:list = None,
    to_do = "0") -> InlineKeyboardMarkup:
    """Возвращает пользователю клавитуру событий

    Args:
        events_list (list): список событий
        results_list (list, optional): список прошедших событий. Defaults to None.
        to_do (str, optional): что нужно сделать с конкурсом. Defaults to "0".

    Returns:
        InlineKeyboardMarkup: Клавитура событий
    TODO: Добавить кнопку возврата в меню администратора
    """

    markup = InlineKeyboardMarkup(row_width=1)
    for event in events_list:
        if event['item_id'] in results_list:
            markup.insert(
                InlineKeyboardButton(
                    text="✅    " + event['name'],
                    callback_data = make_callback_data_ap(
                        to_do = to_do,
                        event_id = event['item_id']
                    )
                )
            )
        else:
            markup.insert(
                InlineKeyboardButton(
                    text="📝    " + event['name'],
                    callback_data = make_callback_data_ap_events(
                        to_do=to_do,
                        event_id = event['item_id']
                    )
                )
            )
    markup.insert(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data_ap()
        )
    )
    return markup




async def ap_chcek_result() -> InlineKeyboardMarkup:
    """Клавиатура для перехода к проверке введеных результатов

    Returns:
        InlineKeyboardMarkup: [description]
    """
    markup = InlineKeyboardMarkup(row_width=1)
    to_do = [
        {'name':"Все верно", 'to_do':"save"},
        {'name':"начать ввод заново",'to_do':"repeat"}
    ]
    for item in to_do:
        markup.insert(
            InlineKeyboardButton(
                text=item['name'],
                callback_data=make_callback_data_ap(
                    to_do=item['to_do']
                )
            )
        )
    return markup
