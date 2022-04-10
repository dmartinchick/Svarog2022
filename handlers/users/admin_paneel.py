"""Хэндлеры управления админ панелью"""
import logging
from aiogram import types
from keyboards.inline.inline_admin_panel import admin_panel_keyboard

from loader import dp
from utils.db_api.db_comands import get_admin_list


@dp.message_handler(commands="admin_panel")
async def show_admin_panel(message: types.Message):
    """Функция отображения панели адменистратора

    Args:
        message (types.Message): [description]
    """

    user_id = message.from_user.id
    # проверка имеется ли у пользователя админ права
    admins_list = get_admin_list()

    if user_id in admins_list:
        markup = await admin_panel_keyboard()
        await message.answer(
            text="Панель администратора",
            reply_markup=markup
        )
    else:
        await message.answer(
            text="К сожалению у вас нет прав доступа. "\
                + "Для получения прав администатора - "\
                    + "обратитесь к главному судье фестиваля")


@dp.callback_query_handler(text_contains="set_fol")
async def show_set_fol(call: types.CallbackQuery):
    """Функция вызова меню добавления штрафов"""

    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    await call.message.answer(
        text="Меню добавления штрафов"
    )


@dp.callback_query_handler(text_contains="changing_shedule")
async def show_changing_shedule(call: types.CallbackQuery):
    """Функция вызова меню изменения расписания

    Args:
        call (types.CallbackQuery): [description]
    """

    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    await call.message.answer(
        text="Меню изменения расписания"
    )


@dp.callback_query_handler(text_contains="emergency_message")
async def show_emergency_message(call: types.CallbackQuery):
    """Функция вызова меню отправки экстренных сообщений

    Args:
        call (types.CallbackQuery): [description]
    """

    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    await call.message.answer(
        text="Меню отправки экстренного сообщения"
    )
