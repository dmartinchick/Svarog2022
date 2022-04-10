"""Пакет управления функцией администратора 'ОБновить результат'"""
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards.inline.inline_admin_panel import ap_event_keyboard, ap_result_keyboard

from loader import dp
from utils.db_api.db_comands import get_event_name, get_event_results, get_result_list, get_team_name_from_result

class UpdateResult(StatesGroup):
    """Класс для обновления результатов

    Args:
        StatesGroup (_type_): _description_
    """
    event_name = State()
    result_id = State()
    set_update = State()
    check_update = State()


@dp.callback_query_handler(text_contains="ap:update_result", state=None)
async def ap_update_result_start(call: types.CallbackQuery):
    """Функция вызова меню обновления результатов

    Args:
        call (types.CallbackQuery): [description]
    """

    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    to_do = call.data.split(':')[1]
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
        results_list=[],
        to_do = to_do
    )
    await call.message.answer(
        text="Выбирите конкурс, резьтат которого хотите обновить",
        reply_markup=markup
    )
    await UpdateResult.event_name.set()


@dp.callback_query_handler(state=UpdateResult.event_name)
async def event_update_choosen(call:types.CallbackQuery ,state:FSMContext):
    """Добавляет выбранный конкурс в FSMContex

    Args:
        call (types.CallbackQuery): _description_
        state (FSMContext): _description_
    """
    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    to_do = call.data.split(':')[1]
    event_id = int(call.data.split(':')[3])
    await state.update_data(
        to_do = call.data.split(':')[1],
        event_id = call.data.split(':')[3]
    )
    event_results_list = get_event_results(event_id)
    markup = await ap_result_keyboard(event_results_list ,to_do, event_id)
    await call.message.answer(
        text="Выбирите результат, который хотите обновить",
        reply_markup=markup
    )
    await UpdateResult.result_id.set()


@dp.callback_query_handler(state=UpdateResult.result_id)
async def set_update(call:types.CallbackQuery, state:FSMContext):
    """добавляет выбраный результат конкурса в FSMContex

    Args:
        call (types.CallbackQuery): _description_
        state (FSMContext): _description_
    TODO: Добавить отоброжение названия команды в ответе пользователю
    """
    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    # to_do = call.data.split(':')[1]
    # event_id = int(call.data.split(':')[3])
    reslt_id = int(call.data.split(':')[4])
    team_name = get_team_name_from_result(reslt_id)
    await state.update_data(result_id = reslt_id)
    await call.message.answer(
        text=f"Введите место которая заняла команда {team_name}"
    )
    await state.finish()

# Выбор конкурса - Done
# Выбор результата - Done
# Ввод измененного результата
# (сохранение)\(повторный ввод) результата
