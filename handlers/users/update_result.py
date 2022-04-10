"""Пакет управления функцией администратора 'ОБновить результат'"""
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards.inline.inline_admin_panel import admin_panel_keyboard, ap_chcek_result, \
    ap_event_keyboard, ap_result_keyboard

from loader import dp
from utils.db_api.db_comands import count_teams, get_event_name, get_event_results, \
    get_result_list, get_team_name_from_result, set_update_result

class UpdateResult(StatesGroup):
    """Класс для обновления результатов

    Args:
        StatesGroup (_type_): _description_
    """
    event_name = State()
    result_id = State()
    set_update = State()
    check_update = State()


@dp.callback_query_handler(text_contains="ap:update_result:save", state=UpdateResult.check_update)
async def save_update(call: types.CallbackQuery, state: FSMContext):
    """Сохронение обновления резльтата в БД

    Args:
        call (types.CallbackQuery): _description_
        state (FSMContext): _description_
    """
    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    data = await state.get_data()
    set_update_result(
        result_id=data['result_id'],
        place=data['update_place'])
    await state.finish()
    markup = await admin_panel_keyboard()
    await call.message.answer(
        text="Обновленный результат сохранен",
        reply_markup=markup
    )


@dp.callback_query_handler(text_contains="ap:update_result:repeat", state=UpdateResult.check_update)
async def repet_entry(call: types.CallbackQuery, state: FSMContext):
    """Повторный выбор конкурса для обновления  результата

    Args:
        call (types.CallbackQuery): _description_
        state (FSMContext): _description_
    """
    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    # создаем список словарей конкурсов результат которых уже введен
    data = await state.get_data()
    to_do = data['to_do']
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
    await state.reset_data()
    await UpdateResult.event_name.set()


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
async def result_update_choosen(call:types.CallbackQuery, state:FSMContext):
    """добавляет выбраный результат конкурса в FSMContex

    Args:
        call (types.CallbackQuery): _description_
        state (FSMContext): _description_
    """
    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    # to_do = call.data.split(':')[1]
    # event_id = int(call.data.split(':')[3])
    result_id = int(call.data.split(':')[4])
    team_name = get_team_name_from_result(result_id)
    await state.update_data(result_id = result_id)
    await call.message.answer(
        text=f"Введите место которая заняла команда {team_name}"
    )
    await UpdateResult.set_update.set()


@dp.message_handler(state=UpdateResult.set_update)
async def set_updated_date(message: types.Message, state: FSMContext):
    """Добавляет обновленное место команды в FSMContex

    Args:
        message (types.Message): место команды, которое ввел пользователь
        state (FSMContext): _description_
    """
    update_place = int(message.text)
    if update_place > 0 and update_place <= count_teams():
        await state.update_data(
            update_place = update_place)
        data = await state.get_data()
        team_name = get_team_name_from_result(data['result_id'])
        event_name = get_event_name(data['event_id'])
        markup = await ap_chcek_result(data['to_do'])
        await message.answer(
            text=f"Команда {team_name} в конкурсе {event_name} заняла {update_place} место?",
            reply_markup=markup
        )
        await UpdateResult.check_update.set()
    else:
        await message.answer(
            text=f"Вы ввели неверное чилсо. Введите место от 1 до {count_teams()}"
        )
        await UpdateResult.set_update.set()
