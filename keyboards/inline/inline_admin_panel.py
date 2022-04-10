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
    to_do_list = [
        {'name':"📝 Добавить результат конкурса", 'to_do_item':"add_result"},
        {'name': "Удалить результат конкруса", 'to_do_item':"claer_result"},
        {'name':"✏ Обновить результат конкурса", 'to_do_item':"update_result"},
        {'name':"Добавить штраф", 'to_do_item':"set_fol"},
        {'name':"🕑 Измененить расписания", 'to_do_item':"changing_shedule"},
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
    results_list:list,
    to_do:str) -> InlineKeyboardMarkup:
    """Возвращает пользователю клавитуру событий

    Args:
        events_list (list): список событий
        results_list (list, optional): список прошедших событий. Defaults to None.
        to_do (str): что нужно сделать с конкурсом.

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
                    callback_data = make_callback_data_ap(
                        to_do=to_do,
                        event_id = event['item_id']
                    )
                )
            )
    return markup


async def ap_chcek_result(to_do:str) -> InlineKeyboardMarkup:
    """Клавиатура для перехода к проверке введеных результатов

    Returns:
        InlineKeyboardMarkup: [description]
    """
    markup = InlineKeyboardMarkup(row_width=1)
    confirmed = [
        {'name':"Все верно", 'confirmed':"save"},
        {'name':"Начать ввод заново",'confirmed':"repeat"}
    ]
    for item in confirmed:
        markup.insert(
            InlineKeyboardButton(
                text=item['name'],
                callback_data=make_callback_data_ap(
                    to_do=to_do,
                    confirmed=item['confirmed']
                )
            )
        )
    return markup


async def ap_result_keyboard(
    event_results_list:list,
    to_do:str,
    event_id:str) -> InlineKeyboardMarkup:
    """возвращает пользователю клавитуру результатов

    Args:
        event_results_list (list): _description_
        to_do (str): что нужно сделать с конкурсом.
        event_id (str): id конкурса

    Returns:
        InlineKeyboardMarkup: Клавиатура результатов
    """
    markup = InlineKeyboardMarkup(row_width=1)
    for result in event_results_list:
        markup.insert(
            InlineKeyboardButton(
                text=f"Команда: {result['team_name']} - место:{result['place']}",
                callback_data=make_callback_data_ap(
                    to_do=to_do,
                    event_id=event_id,
                    result_id=result['result_id']
                )
            )
        )
    return markup
