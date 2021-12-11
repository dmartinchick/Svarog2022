"""Пакет управления функцией администратора 'Добавить результат'"""
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.inline.inline_admin_panel import ap_event_keyboard

from utils.db_api.db_comands import get_teams_list
from loader import dp


class AddResult(StatesGroup):
    """Класс добавления результатов конкурсов

    Args:
        StatesGroup ([type]): [description]
    """
    waiting_for_event_name = State()
    teams_list = get_teams_list()
    for team in teams_list:
        team['item_id'] = State()

@dp.callback_query_handler(text_contains = "add_result")
async def ap_add_result_start(call: types.CallbackQuery):
    """Функция вызова меню добавления результатов

    Args:
        call (types.CallbackQuery): [description]
    TODO: Разобрать с FSMconntex
    """

    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    markup = await ap_event_keyboard()
    await call.message.answer(
        text="Выберите конкурс результат которого вы хотите добавить",
        reply_markup=markup
    )
    await AddResult.next()
