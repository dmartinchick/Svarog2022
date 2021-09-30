from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery
from aiogram.types import user
from aiogram.types.user import User
from utils.db_api.sqlighter import SQL

from loader import dp
from utils.misc.other import get_unsubs_list

from keyboards.inline.subscriptions_menu import categories_keyboard, subscriptions_keyboard, unsubscriptions_keyboard
from keyboards.inline.callback_datas import menu_cd

async def subscriptions_categories(call:CallbackQuery, **kwargs):
    """Формирует и возвращает пользователю клавиатуру категорий
    """
    user_id = call.from_user.id       
    # Формируем клавиатуру
    markup = await categories_keyboard(user_id)
    await call.message.answer(text="Менеджер подписок.\nВыберите интересующую вас категорию.",
                            reply_markup=markup)


async def subscriptions_items(call:CallbackQuery, user_id, category, **kwargs):
    """Формируем и возвращаем пользователю клавиатуру с подписками на команды
    """
    
    sing_markup = await subscriptions_keyboard(category, user_id)
    unsing_markup = await unsubscriptions_keyboard(category, user_id)

    await call.message.answer(text="Вы подписаны на следующие команды. \nЧто бы отписаться нажмите на команду", 
                                reply_markup=sing_markup)
    await call.message.answer(text="Вы не подписаны на следующие команды. \nЧто бы подписаться нажмите на команду",
                                reply_markup=unsing_markup)


@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    # Получаем текущий уровень меню, который запросил пользователь
    current_level = callback_data.get("level")

    # Получаем id пользователя
    user_id = callback_data.get("user_id")

    # Получаем категорию, которую выбрал пользователь (Передается всегда)
    category = callback_data.get("category")

    # Получаем айди товара, который выбрал пользователь (Передается НЕ ВСЕГДА - может быть 0)
    item_id = int(callback_data.get("item_id"))

    # Прописываем "уровни" в которых будут отправляться новые кнопки пользователю
    levels = {
        "0": subscriptions_categories,  # Отдаем категории
        "1": subscriptions_items  # Отдаем список команд/событий 
    }

    # Забираем нужную функцию для выбранного уровня
    current_level_function = levels[current_level]

    await current_level_function(
        call,
        user_id = user_id,
        category=category,
        item_id=item_id
    )
