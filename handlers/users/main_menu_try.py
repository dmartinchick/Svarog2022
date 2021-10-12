from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message, message
from keyboards.inline.inkb_main_menu import main_menu_keyboard
from keyboards.inline.subscriptions_menu import categories_keyboard
from utils.db_api.db_comands import get_date_end, get_date_start, get_what_now

from loader import dp
import logging
from data import config

from datetime import datetime, timedelta



@dp.message_handler(commands=['Меню', 'menu'], commands_prefix = ['⠀','/'])
async def show_main_menu(message: types.Message):
    await main_menu_category(message)


async def main_menu_category(message: Union[CallbackQuery, Message], **kwargs):
    
    # Формируем клавиатуру
    markup = main_menu_keyboard()
    
    # Проверяем, что за тип апдейта. Если Message - отправляем новое сообщение
    if isinstance(message, Message):
        await message.answer("Главное меню", reply_markup=markup)
    
    # Если CallbackQuery - изменяем это сообщение
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)


@dp.callback_query_handler(text_contains="what_now")
async def show_what_now(call: types.CallbackQuery):

    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info(f"{callback_data=}")

    tdate = datetime.now() + timedelta(hours=config.DELTA)

    # получаем дату и время начала и конца фестиваля
    festival_start = get_date_start()
    festival_end = get_date_end()

    # Проверяем начался/закончился ли фестиваль
    if tdate < festival_start:
        await call.message.answer("😁 Фестиваль еще не начался, \nЗагляни сюда 18 июня!")
    elif tdate > festival_end:
        await call.message.answer("☹ К сожелению, фестиваль уже прошел.\nУвидимся в следующем году! 😁")
    else:
        await call.message.answer(text='🤓 Сейча проходит 🤓')
        
        # Получаем список текущих событий
        event_now_list = get_what_now(tdate)
        for event in event_now_list:
            await call.message.edit_text(text=event)  
    pass