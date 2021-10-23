from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.callback_query import CallbackQuery
from aiogram.utils.callback_data import CallbackData

main_menu_cb = CallbackData("show_menu", "level", "category", "subcategory", "to_do", "item_id")

def make_callback_data(level, category="0", subcategory="0", to_do="0", item_id="0"):
    """формирует callback_data
    """
    return main_menu_cb.new(level=level, 
                            category=category, 
                            subcategory=subcategory, 
                            to_do=to_do, item_id=item_id)


# Создаем клавиатуру главного меню
async def main_menu_keyboard():
    """Формирует клавиатуру главного меню

    Args:
        category ([type]): [description]

    Returns:
        [type]: [description]
    """
    CURENT_LEVEL = 0

    markup = InlineKeyboardMarkup(row_width=1)

    categorys = [
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

    for category in categorys:
        button_text = category['name']
        button_callback_data = make_callback_data(level = CURENT_LEVEL+1, category=category['category_item'])
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=button_callback_data)
        )
    
    return markup

# Создаем клавиатуру категорий
async def category_keyboard(call: CallbackQuery, category, **kwargs):
    # CURENT_LEVEL = 1
    pass

async def subcategory_keyboard():
    pass