from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


from keyboards.inline.callback_datas import menu_cd, sing_item, unsing_item
from utils.db_api.sqlighter import SQL
from utils.misc.other import get_unsubs_list


# menu_cd = CallbackData("show_menu", "level", "category", "item_id")
# sing_item = CallbackData("sing", "item")
# unsing_item = CallbackData("unsing", "item")

# С помощью этой функции будем формировать коллбек дату для каждого элемента меню, в зависимости от
# переданных параметров. Если Подкатегория, или айди товара не выбраны - они по умолчанию равны нулю
def make_callback_data(level, user_id, category="0", item_id="0"):
    return menu_cd.new(level=level, user_id=user_id, category=category, item_id=item_id)

# Создаем функцию, которая отдает клавиатуру с доступными категориями
async def categories_keyboard(user_id):
    # Текущий уровень
    CURRENT_LAVEL = 0

    # Создаем клавиатуру
    markup = InlineKeyboardMarkup(row_width=1)
    categories = [{'name':"Подписки на команды", 'name_en':"team_subs"}, 
                {'name':"Подписки на конкурсы", 'name_en':"event_subs"}]
    for category in categories:
        # Формируем текст кнопки
        button_text = category['name']
        # Формируем callback_data
        callback_data = make_callback_data(level=CURRENT_LAVEL+1,
                                            user_id=user_id,
                                            category=category['name_en'])

        # Вставляем кнопку в клавиатуру
        markup.insert(
            InlineKeyboardButton(text=button_text,callback_data=callback_data)
        )
    
    # Возвращаем клавиатуру
    return markup

# Функция с активными подписками
async def subscriptions_keyboard(category, user_id):
    # текущий уровень
    CURRENT_LAVEL = 1

    # Создаем клавиатуру
    markup = InlineKeyboardMarkup(row_width=2)
    if category == 'team_subs':
        user_sings = SQL.get_team_subs(user_id)
    elif category == 'event_subs':
        user_sings = SQL.get_event_subs(user_id)

    for sing in user_sings:
        # Формируем название кнопки
        button_text = sing['name']
        # Формируем callback
        call_back = sing_item.new(user_id=user_id,
                            category=category, 
                            item=sing['id'])
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=call_back)
        )
    
    # Формируем конпку "Назад" 
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LAVEL-1,
                                            user_id=user_id)
        )
    ) 

    return markup


# Функция с неактивными подписками
async def unsubscriptions_keyboard(category, user_id):
    # текущий уровень
    CURRENT_LAVEL = 1

    # Создаем клавиатуру
    markup = InlineKeyboardMarkup(row_width=2)
    if category == 'team_subs':
        team_list = SQL.get_teams_all()
        user_sings = SQL.get_team_subs(user_id)
        user_unsing = get_unsubs_list(team_list, user_sings)

    elif category == 'event_subs':
        event_list = SQL.get_events_all()
        user_sings = SQL.get_event_subs(user_id)
        user_unsing = get_unsubs_list(event_list, user_sings)
        
    for sing in user_unsing:
        # Формируем название кнопки
        button_text = sing['name']
        # Формируем callback
        call_back = unsing_item.new(user_id=user_id, 
                                    category=category,
                                    item=sing['id'])
        markup.insert(
            InlineKeyboardButton(text=button_text,callback_data=call_back)
        )
    # Формируем кнопку назад
    markup.row(
        InlineKeyboardButton(text="Назад", callback_data=make_callback_data(level=CURRENT_LAVEL-1,
                                                                            user_id=user_id,
                                                                            category=category))
    )

    return markup
