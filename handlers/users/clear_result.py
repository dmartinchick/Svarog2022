"""Пакет управления функцией администратора 'Удалить результат конкруса'"""
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards.inline.inline_admin_panel import admin_panel_keyboard, \
    ap_chcek_result, ap_event_keyboard

from loader import dp
from utils.db_api.db_comands import delete_event_result, get_event_name, get_result_list

class ClearResult(StatesGroup):
    """Класс для удаления результатов

    Args:
        StatesGroup (_type_): _description_
    """
    event_name = State()
    check_delete = State()


@dp.callback_query_handler(text_contains = "ap:claer_result:save", state=ClearResult.check_delete)
async def save_delete_result(call: types.CallbackQuery, state: FSMContext):
    """Удаление результатов из БД

    Args:
        call (types.CallbackQuery): _description_
        state (FSMContext): _description_
    """
    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    data = await state.get_data()
    event_id = int(data['event_id'])
    delete_event_result(event_id=event_id)
    await state.finish()
    markup = await admin_panel_keyboard()
    await call.message.answer(
        text="Результаты удалены\n"\
            "Панель администратора",
        reply_markup=markup
    )


@dp.callback_query_handler(text_contains = "ap:claer_result:repeat", state=ClearResult.check_delete)
async def repeat_delete_result(call: types.CallbackQuery, state: FSMContext):
    """Повторный выбор результата конкурса для удаления

    Args:
        call (types.CallbackQuery): _description_
        state (FSMContext): _description_
    """
    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    to_do = call.data.split(':')[1]
    await state.reset_data()

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
        text="Выбирите конкурс, резьтат которого ходите удалить",
        reply_markup=markup
    )
    await ClearResult.event_name.set()



@dp.callback_query_handler(text_contains="ap:claer_result", state=None)
async def ap_clear_result_start(call: types.CallbackQuery):
    """Функция вызова меню удаления результатов

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
        text="Выбирите конкурс, резьтат которого хотите удалить",
        reply_markup=markup
    )
    await ClearResult.event_name.set()


@dp.callback_query_handler(state=ClearResult.event_name)
async def event_delete_choosen(call: types.CallbackQuery, state:FSMContext):
    """Добавляет выбранный конкурс в FSMContex

    Args:
        call (types.CallbackQuery): _description_
        state (FSMContext): _description_
    """

    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    to_do = call.data.split(':')[1]
    event = int(call.data.split(':')[3])
    event_name = get_event_name(event)
    await state.update_data(event_id = event)
    markup = await ap_chcek_result(to_do = to_do)
    await call.message.answer(
        text=f"Вы уверены, что хотите удалить результат конкруса {event_name} ?",
        reply_markup=markup
    )
    await ClearResult.check_delete.set()
