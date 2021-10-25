"""Создание клавиатуры главного меню"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.db_api.db_comands import get_events_list, get_signed_events_list
from utils.db_api.db_comands import get_signed_teams_list, get_teams_list
from utils.db_api.db_comands import get_unsigned_events_list, get_unsigned_teams_list
from keyboards.inline.callback_datas import main_menu_choice, main_menu_cb

def make_callback_data(level,category = 0,subcategory = 0,item = 0):
    """Формирует callback_data, подставля вместо отсутствующих значений '0'."""
    return main_menu_cb.new(
        level = level,
        category = category,
        subcategory = subcategory,
        item = item
    )

async def main_menu_keyboard():
    """Возвращает пользователю клавиатуру главного меню"""
    # Указываем текущий уровень
    CURENT_LEVEL = 0
    markup = InlineKeyboardMarkup(
        row_width = 1
    )
    categories = [
        {'name':"Что сейчас происходит", 'category_item':"what_now"},
        {'name':"Ближайшие мероприятия",'category_item':"what_next"},
        {'name':"Полное расписание",'category_item':"full_shedule"},
        {'name':"Результаты",'category_item':"result"},
        {'name':"Конкурсы",'category_item':"event"},
        {'name':"Команды",'category_item':"team"},
        {'name':"Менеджер подписок",'category_item':"subscriptions_manager"},
        {'name':"Карта фестиваля",'category_item':"map"},
        {'name':"Поделиться ссылкой",'category_item':"share"},
        {'name':"Положение фестиваля",'category_item':"about"}
    ]
    for category in categories:
        button_text = category['name']
        button_callback_data = make_callback_data(
            level=CURENT_LEVEL + 1,
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
    CURENT_LEVEL = 1
    markup = InlineKeyboardMarkup(
        row_width = 1
    )
    result_subcategories = [
        {'name' : "Кубок фестиваля", 'subcategory_item' : "festival_cup"},
        {'name' : "Кубок холдинга", 'subcategory_item' : "holding_cup"},
        {'name' : "Кубок туризма", 'subcategory_item' : "tourism_cup"},
        {'name' : "Кубок спорта", 'subcategory_item' : "sport_cup"},
        {'name' : "Кубок культуры", 'subcategory_item': "culture_cup"},
    ]
    for subcategory in result_subcategories:
        button_text = subcategory['name']
        button_callback_data = make_callback_data(
            level = CURENT_LEVEL + 1,
            category = category,
            subcategory = subcategory['subcategory_item'])
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
                level = CURENT_LEVEL-1)
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
    CURENT_LEVEL = 1
    markup = InlineKeyboardMarkup(
        row_width=1
    )
    events = get_events_list()
    for event in events:
        button_text = event['name']
        button_callback_data = make_callback_data(
            level=CURENT_LEVEL + 1,
            category=category,
            subcategory=event['event_id']
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
                level=CURENT_LEVEL - 1
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
    CURENT_LEVEL = 1
    markup = InlineKeyboardMarkup(
        row_width=1
    )
    teams = get_teams_list()
    for team in teams:
        button_text = team['name']
        button_callback_data = make_callback_data(
            level=CURENT_LEVEL + 1,
            category=category,
            subcategory=team['team_id']
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
                level = CURENT_LEVEL - 1
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
    CURENT_LEVEL = 1
    markup = InlineKeyboardMarkup(
        row_width=1
    )
    subscriptions_manager_subcategories= [
        {'name':"Подписки на команды",'subcategory_item':"subscription_manager_team"},
        {'name':"Подписки на конкурсы",'subcategory_item':"subscription_manager_event"}
    ]
    for subcategory in subscriptions_manager_subcategories:
        button_text=subcategory['name']
        button_callback_data = make_callback_data(
            level=CURENT_LEVEL + 1,
            category=category,
            subcategory=subcategory['subcategory_item']
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
                level = CURENT_LEVEL - 1
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

    TODO:
        Реализовать button_callback_data
    """
    CURENT_LEVEL = 2
    markup = InlineKeyboardMarkup(
        row_width=2
    )
    # Получение списка конкурсов или команд
    if category == "event":
        items_list = get_signed_events_list(user_id)
    else:
        items_list = get_signed_teams_list(user_id)
    for item in items_list:
        button_text = item['name']
        button_callback_data = ""
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
                level = CURENT_LEVEL - 1,
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
        Реализовать button_callback_data
    """
    CURENT_LEVEL = 2
    markup = InlineKeyboardMarkup(
        row_width=2
    )
    if category == "event":
        items_list = get_unsigned_events_list(user_id)
    else:
        items_list = get_unsigned_teams_list(user_id)
    for item in items_list:
        button_text = item['name']
        button_callback_data = ''
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
                level=CURENT_LEVEL -1,
                category=category,
                subcategory=subcategory
            )
        )
    )
    return markup

inkb_main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Что сейчас происходит",
                callback_data=main_menu_choice.new(category_name="what_now")),
        ],
        [
            InlineKeyboardButton(
                text="Ближайшие мероприятия",
                callback_data="main:what_next"),
        ],
        [
            InlineKeyboardButton(
                text="Полное расписание",
                callback_data="main:full_schedule"),
        ],
        [
            InlineKeyboardButton(
                text="Результаты",
                callback_data="main:results"),
        ],
        [
            InlineKeyboardButton(
                text="Конкурсы",
                callback_data="main:contests"),
        ],
        [
            InlineKeyboardButton(
                text="Команды",
                callback_data="main:team"),
        ],
        [
            InlineKeyboardButton(
                text="Менеджер подписок",
                callback_data="main:subscriptions_manager"),
        ],
        [
            InlineKeyboardButton(
                text="Карта фестиваля",
                callback_data="main:map"),
        ],
        [
            InlineKeyboardButton(
                text="Поделиться ссылкой",
                callback_data="main:share"),
        ],
        [
            InlineKeyboardButton(
                text="Положения фестиваля",
                callback_data="main:about")
        ]
    ]
)
