"""Пакет управления функцией администратора 'удалить результат'"""
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards.inline.inline_admin_panel import ap_event_keyboard

from loader import dp
from utils.db_api.db_comands import get_event_name, get_result_list


class ClearResult(StatesGroup):
    """Класс удаления результатов конкурса

    Args:
        StatesGroup (_type_): _description_
    """
    event_name = State()
    check_delete = State()


@dp.callback_query_handler(text_contains="ap:claer_result", state=None)
async def ap_clear_result_start(call: types.CallbackQuery):
    """Функция вызова меню удаления результатов

    Args:
        call (types.CallbackQuery): [description]
    """

    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)
    # создаем список словарей конкурсов результат которых уже введен
    results_list = []
    results_list_id = get_result_list()
    for result in results_list_id:
        results_list.append(
            {'name':get_event_name(result),
            'item_id':result}
        )
    markup = await ap_event_keyboard(
        events_list=results_list,
        results_list=results_list_id,
        to_do = "clear_result")
    await call.message.answer(
        text="Меню удаления результатов",
        reply_markup=markup
    )
    await ClearResult.event_name.set()


@dp.callback_query_handler(state=ClearResult.event_name)
async def event_choosen(call:types.CallbackQuery, state: FSMContext):
    """добавляет выбраный конкурс в FSM Storege

    Args:
        call (types.CallbackQuery): данные callback
        state (FSMContext): [description]
    TODO: Добавить переход к следующему шагу
    """
    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)
    event = int(call.data.split(':')[2])
    await state.update_data(event_id = event)
    await ClearResult.check_delete.set()
