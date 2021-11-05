"""Создание клавиатуры главного меню"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.db_api.db_comands import get_events_list, get_signed_events_list
from utils.db_api.db_comands import get_signed_teams_list, get_teams_list
from utils.db_api.db_comands import get_unsigned_events_list, get_unsigned_teams_list
from keyboards.inline.callback_datas import make_callback_data


async def main_menu_keyboard() -> InlineKeyboardMarkup:
    """Возвращает пользователю клавиатуру главного меню

    Returns:
        InlineKeyboardMarkup: Клавиатура со списком категорий
    """
    # Указываем текущий уровень
    curent_level = 0
    markup = InlineKeyboardMarkup(
        row_width=1
    )
    categories = [
        {'name':"Что сейчас происходит", 'category_item':"what_now"},
        {'name':"Ближайшие мероприятия",'category_item':"what_next"},
        {'name':"Полное расписание",'category_item':"full_shedule"},
        {'name':"Результаты",'category_item':"result"},
        {'name':"Конкурсы",'category_item':"event"},
        {'name':"Команды",'category_item':"team"},
        {'name':"Менеджер подписок",'category_item':"sm"},
        {'name':"Карта фестиваля",'category_item':"map"},
        {'name':"Поделиться ссылкой",'category_item':"share"},
        {'name':"Положение фестиваля",'category_item':"about"}
    ]
    for category in categories:
        button_text = category['name']
        button_callback_data = make_callback_data(
            level=curent_level + 1,
            category=category['category_item'])
        markup.insert(
            InlineKeyboardButton(
                text=button_text,
                callback_data=button_callback_data)
        )
    return markup


async def result_keyboard(category:str) -> InlineKeyboardMarkup:
    """Создает клавиатуру меню результатов

    Args:
        category (str): раздел главного меню 'Результаты'

    Returns:
        InlineKeyboardMarkup: клавиатура со списком подкатегорий результатов
    """
    curent_level = 1
    markup = InlineKeyboardMarkup(
        row_width = 1
    )
    result_subcategories = [
        {'name' : "Кубок фестиваля", 'subcategory' : "festival_cup"},
        {'name' : "Кубок холдинга", 'subcategory' : "holding_cup"},
        {'name' : "Кубок туризма", 'subcategory' : "tourism_cup"},
        {'name' : "Кубок спорта", 'subcategory' : "sport_cup"},
        {'name' : "Кубок культуры", 'subcategory': "culture_cup"},
    ]
    for subcategory in result_subcategories:
        button_text = subcategory['name']
        button_callback_data = make_callback_data(
            level = curent_level + 1,
            category = category,
            subcategory = subcategory['subcategory'])
        markup.insert(
            InlineKeyboardButton(
                text=button_text,
                callback_data=button_callback_data
            )
        )
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(
                level = curent_level-1)
        )
    )
    return markup


async def event_keyboard(category:str) -> InlineKeyboardMarkup:
    """Создает клавиатуру со списком конкурсов

    Args:
        category (str): раздел главного меню 'Конкурсы'

    Returns:
        markup[InlineKeyboardMarkup]: клавиатура cо списком конкурсов
    """
    curent_level = 1
    markup = InlineKeyboardMarkup(
        row_width=1
    )
    events = get_events_list()
    for event in events:
        button_text = event['name']
        button_callback_data = make_callback_data(
            level= curent_level + 2, # +2, т.к. необходимо перейти к выводу информации
            category=category,
            action="show",
            item_id=event["item_id"]
        )
        markup.insert(
            InlineKeyboardButton(
                text=button_text,
                callback_data=button_callback_data
            )
        )
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(
                level=curent_level - 1
            )
        )
    )
    return markup


async def team_keyboard(category:str) -> InlineKeyboardMarkup:
    """Создает клавиатуру меню команд

    Args:
        category (str): раздел главного меню 'Команды'

    Returns:
        InlineKeyboardMarkup: Клавиатура со списком команд
    """
    curent_level = 1
    markup = InlineKeyboardMarkup(
        row_width=2
    )
    teams = get_teams_list()
    for team in teams:
        button_text = team['name']
        button_callback_data = make_callback_data(
            level=curent_level + 2, # +2, т.к. необходимо перейти выводу информации
            category= category,
            action="show",
            item_id=team["item_id"]
        )
        markup.insert(
            InlineKeyboardButton(
                text=button_text,
                callback_data=button_callback_data
            )
        )
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(
                level = curent_level - 1
            )
        )
    )
    return markup


async def subscriptions_manager_keyboard(category:str) -> InlineKeyboardMarkup:
    """Создает клавиатуру менеджера подписок

    Args:
        category (str): раздел главного меню 'Менеджер подписок'

    Returns:
        InlineKeyboardMarkup: клавиатура со списком подкатегорий менеджера подписок
    """
    curent_level = 1
    markup = InlineKeyboardMarkup(
        row_width=1
    )
    subscriptions_manager_subcategories= [
        {'name':"Подписки на команды",'subcategory':"sm_team"},
        {'name':"Подписки на конкурсы",'subcategory':"sm_event"}
    ]
    for subcategory in subscriptions_manager_subcategories:
        button_text=subcategory['name']
        button_callback_data = make_callback_data(
            level=curent_level + 1,
            category=category,
            subcategory=subcategory['subcategory']
        )
        markup.insert(
            InlineKeyboardButton(
                text=button_text,
                callback_data=button_callback_data
            )
        )
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(
                level = curent_level - 1
            )
        )
    )
    return markup


async def signed_to_item(category:str, subcategory:str, user_id:int) -> InlineKeyboardMarkup:
    """Создает клавиатуру с командами или конкурсами на которые подписан пользователь

    Args:
        category (str): раздел главного меню
        subcategory (str): раздел меню менеджера подписок
        user_id (int): id пользователя

    Returns:
        InlineKeyboardMarkup: Клавиатура со списком команд или конкурсов
         на которые подписан пользователь
    """
    curent_level = 2
    markup = InlineKeyboardMarkup(
        row_width=2
    )
    # Получение списка конкурсов или команд
    if subcategory == "sm_event":
        items_list = get_signed_events_list(user_id)
    elif subcategory == "sm_team":
        items_list = get_signed_teams_list(user_id)
    else:
        print("!!!! Что то пошло не так!!!!")
    for item in items_list:
        button_text = item['name']
        button_callback_data = make_callback_data(
            level = curent_level + 1,
            category=category,
            subcategory=subcategory,
            action="unsubscribe",
            item_id=item["item_id"]
        )
        markup.insert(
            InlineKeyboardButton(
                text=button_text,
                callback_data=button_callback_data
            )
        )
    markup.row(
        InlineKeyboardButton(
            text = "Назад",
            callback_data = make_callback_data(
                level = curent_level - 1,
                category=category,
                subcategory=subcategory
            )
        )
    )
    return markup


async def unsigned_to_item(category:str, subcategory:str, user_id:int) -> InlineKeyboardMarkup:
    """Создает клавиатуру с командами или конкурсами на которые не подписан пользователь

    Args:
        category (str): раздел главного меню
        subcategory (str): раздел меню менеджера подписок
        user_id (int): id пользователя

    Returns:
        InlineKeyboardMarkup: Клавиатура со списком команд или конкурсов
         на которые не подписан пользователь

    TODO:
        1. Реализовать button_callback_data
        2. Не уверен насчет успешности реализации
    """
    curent_level = 2
    markup = InlineKeyboardMarkup(
        row_width=2
    )
    if subcategory == "sm_event":
        items_list = get_unsigned_events_list(user_id)
    elif subcategory == "sm_team":
        items_list = get_unsigned_events_list(user_id)
    else:
        print("!!!! Что то пошло не так !!!!")
    for item in items_list:
        button_text = item['name']
        button_callback_data = make_callback_data(
            level = curent_level + 1,
            category=category,
            subcategory=subcategory,
            action="subscribe",
            item_id=item["item_id"]
        )
        markup.insert(
            InlineKeyboardButton(
                text=button_text,
                callback_data=button_callback_data
            )
        )
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(
                level=curent_level -1,
                category=category,
                subcategory=subcategory
            )
        )
    )
    return markup
