"""Пакет управления функцией администратора 'Обновить расписание'"""
from datetime import datetime
import logging


from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.inline.inline_admin_panel import admin_panel_keyboard, ap_chcek_result, \
    ap_schedule_keyboard

from loader import dp
from utils.db_api.db_comands import get_schedule_event_name, get_schedule_list, set_update_schedule

class UpdateShedule(StatesGroup):
    """Класс для изменения расписания"""
    event_name = State()
    updated_datetime_start = State()
    updated_datetime_end = State()
    check_update_schedule = State()


@dp.callback_query_handler(
    text_contains="ap:update_schedule:save",
    state=UpdateShedule.check_update_schedule
)
async def save_update_schedule(call:types.CallbackQuery, state: FSMContext):
    """Созраниение измененного расписания в БД

    Args:
        call (types.CallbackQuery): _description_
        state (FSMContext): _description_
    """
    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    data = await state.get_data()
    set_update_schedule(
        int(data['schedule_id']),
        data['datetime_start'],
        data['datetime_end']
    )
    await state.finish()
    markup = await admin_panel_keyboard()
    await call.message.answer(
        text="Расписание обновленно",
        reply_markup=markup
    )


@dp.callback_query_handler(
    text_contains="ap:update_schedule:repeat",
    state=UpdateShedule.check_update_schedule
)
async def repeat_update_schedule(call:types.CallbackQuery, state: FSMContext):
    """Созраниение измененного расписания в БД

    Args:
        call (types.CallbackQuery): _description_
        state (FSMContext): _description_
    """
    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    data = await state.get_data()
    to_do = data['to_do']
    schedule_list = get_schedule_list()
    markup = await ap_schedule_keyboard(schedule_list, to_do)
    await call.message.answer(
        text="Выбирите мероприятие, которое необходимо изменить",
        reply_markup=markup
    )
    await state.reset_data()
    await UpdateShedule.event_name.set()


@dp.callback_query_handler(text_contains="ap:update_schedule", state=None)
async def ap_update_shedule_start(call: types.CallbackQuery):
    """Функция вызова меню изменения расписания

    Args:
        call (types.CallbackQuery): [description]
    """

    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    to_do = call.data.split(':')[1]
    schedule_list = get_schedule_list()
    markup = await ap_schedule_keyboard(schedule_list, to_do)
    await call.message.answer(
        text="Выбирите мероприятие, которое необходимо изменить",
        reply_markup=markup
    )
    await UpdateShedule.event_name.set()

@dp.callback_query_handler(state=UpdateShedule.event_name)
async def schedule_update_choosen(call: types.CallbackQuery, state: FSMContext):
    """Сохранение id расписания в FSMContex

    Args:
        call (types.CallbackQuery): _description_
        state (FSMContext): _description_
    """
    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    to_do = call.data.split(':')[1]
    schedule_id = call.data.split(':')[3]
    await state.update_data(
        to_do = to_do,
        schedule_id = schedule_id
    )
    await call.message.answer(
        text="Укажите дату и время начала меропрития "\
            f"{get_schedule_event_name(schedule_id)}"\
                " в формате дд.мм.гггг чч:мм"
    )
    await UpdateShedule.updated_datetime_start.set()


@dp.message_handler(state=UpdateShedule.updated_datetime_start)
async def update_datetime_start(message: types.Message, state: FSMContext):
    """Добавление обновленного времени и даты начала в FSMContex

    Args:
        message (types.Message): _description_
        state (FSMContext): _description_
    """
    try:
        updated_datetime_start = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
    except ValueError:
        data = await state.get_data()
        await message.answer(
            text="‼ Вы указали неверную дату ‼\n"\
                "Укажите дату и время начала меропрития "\
                f"{get_schedule_event_name(data['schedule_id'])}"\
                    " в формате дд.мм.гггг чч:мм"
        )
        await UpdateShedule.updated_datetime_start.set()

    await state.update_data(
        datetime_start = updated_datetime_start
    )
    data = await state.get_data()
    await message.answer(
        text="Укажите дату и время окончания меропрития "\
            f"{get_schedule_event_name(data['schedule_id'])}"\
                " в формате дд.мм.гггг чч:мм"
    )
    await UpdateShedule.updated_datetime_end.set()


@dp.message_handler(state=UpdateShedule.updated_datetime_end)
async def update_datetime_end(message: types.Message, state: FSMContext):
    """Добавление обновленного времени и даты окончания в FSMContex

    Args:
        message (types.Message): _description_
        state (FSMContext): _description_
    """
    try:
        updated_datetime_end = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
    except ValueError:
        data = await state.get_data()
        await message.answer(
            text="‼ Вы указали неверную дату ‼\n"\
                "Укажите дату и время окончания меропрития "\
                f"{get_schedule_event_name(data['schedule_id'])}"\
                " в формате дд.мм.гггг чч:мм"
        )
        await UpdateShedule.updated_datetime_end.set()

    await state.update_data(
        datetime_end = updated_datetime_end
    )
    data = await state.get_data()
    markup = await ap_chcek_result(data['to_do'])
    await message.answer(
        text=f"{get_schedule_event_name(data['schedule_id'])}\n"\
            f"начало: {data['datetime_start']}\n"\
                f"Окончание: {data['datetime_end']}\n"\
                    "Все верно?",
        reply_markup=markup
    )
    await UpdateShedule.check_update_schedule.set()
