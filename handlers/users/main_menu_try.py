from typing import Union

import logging
from datetime import datetime, timedelta

from aiogram import types
from aiogram.types import CallbackQuery, Message
from keyboards.inline.inkb_main_menu import main_menu_keyboard
from keyboards.inline.inkb_event import ink_event_card
from keyboards.inline.subscriptions_menu import categories_keyboard
from utils.db_api.db_comands import get_date_end, get_date_start, get_what_now

from loader import dp
from data import config




async def main_menu_category(message: Union[CallbackQuery, Message], **kwargs):
    """Формирует клавиатуру Главного меню бота

    Args:
        message (Union[CallbackQuery, Message]): [description]
    """
    # Формируем клавиатуру
    markup = main_menu_keyboard(**kwargs)
    # Проверяем, что за тип апдейта. Если Message - отправляем новое сообщение
    if isinstance(message, Message):
        await message.answer("Главное меню", reply_markup=markup)
    # Если CallbackQuery - изменяем это сообщение
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.answer(text="Главное меню", reply_markup=markup)


@dp.message_handler(commands=['Меню', 'menu'], commands_prefix = ['⠀','/'])
async def show_main_menu(message: types.Message):
    """Обрабатывает хэндлер меню, и вызывает функцию, которая формирует клавиатуру главного меню
    """
    await main_menu_category(message)


@dp.callback_query_handler(text_contains="what_now")
async def show_what_now(call: types.CallbackQuery):
    """Показывет ВСЕ события, которые проходят в настоящий момент
    """
    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info(f"{callback_data=}")

    tdate = datetime.now() + timedelta(hours=config.DELTA)

    # получаем дату и время начало и конца фестиваля
    festival_start = get_date_start()
    festival_end = get_date_end()

    # Проверяем начался/закончился ли фестиваль
    if tdate < festival_start:
        await call.message.answer("😁 Фестиваль еще не начался, \nЗагляни сюда 18 июня!")
    elif tdate > festival_end:
        await call.message.answer(
            text="☹ К сожелению, фестиваль уже прошел.\nУвидимся в следующем году! 😁")
    else:
        await call.message.answer(text='🤓 Сейча проходит 🤓')
        # Получаем список текущих событий
        event_now_list = get_what_now(tdate)
        for event in event_now_list:
            #TODO: реализовать клавиатуру для карточки события. кнопки Подписаться|отписаться, подробнее
            await call.message.answer(text=event['name'], reply_markup=ink_event_card)


@dp.callback_query_handler(text_contains="what_next")
async def show_what_next(call: types.CallbackQuery):
    """Возвращает сообщения с 2-мя ближайшими мероприятиями (и показывает сколько времени до них осталось)
    """
    pass


@dp.callback_query_handler(text_contains="full_shedule")
async def show_full_schedule(call: types.CallbackQuery):
    """Возвращает сообщение с картинкой с полным расписание фестиваля
    """
    pass


@dp.callback_query_handler(text_contains="map")
async def show_map(call: types.CallbackQuery):
    """Возвращает сообщение с картинкой картой фестиваля
    """
    pass


@dp.callback_query_handler(text_contains="share")
async def show_share(call: types.CallbackQuery):
    """Возвращает сообщение с картинкой в виде QR-кода со ссылкой на бота
    """
    pass


@dp.callback_query_handler(text_contains="about")
async def show_about(call: types.CallbackQuery):
    """Возвращает сообщение прикрепленым файлом "Положение туристического фестиваля"
    """
    pass
