"""Пакет управления функцией администратора 'Добавить результат'"""
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards.inline.inline_admin_panel import ap_event_keyboard

from loader import dp


class AddResult(StatesGroup):
    """Класс добавления результатов конкурсов

    Args:
        StatesGroup ([type]): [description]
    """
    event_name = State()
    prokat_place = State()
    gks_place = State()
    stal_place = State()
    razam_place = State()
    belvtorcherme_place = State()
    mpz_place = State()
    zubry_place = State()
    rmz_place = State()
    bycord_place = State()
    integral_place = State()
    mzkt_place = State()
    maz_place = State()
    mogilevliftmash_place = State()
    mmz_place = State()
    save_results = State()


@dp.callback_query_handler(text_contains = "add_result", state=None)
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
    await AddResult.event_name.set()


@dp.callback_query_handler(state = AddResult.event_name)
async def event_choosen(call: types.CallbackQuery, state: FSMContext):
    """добавляет выбраный конкурс в FSM Storege

    Args:
        call (types.CallbackQuery): данные callback
        state (FSMContext): [description]
    """
    await state.update_data(event_id = int(call.data.split(':')[1]))

    await call.message.answer(
        text="Какое место заняла команда Прокат?"
    )

    await AddResult.prokat_place.set()


@dp.message_handler(state=AddResult.prokat_place)
async def prokat_place_choosen(message: types.Message, state: FSMContext):
    """добавляет в FSM Storege место которое заняла команда Прокат

    Args:
        message (types.Message): [description]
        state (FSMContext): [description]
    """
    answer = int(message.text)

    if answer > 0 and answer < 16:
        await state.update_data(prokat_place = answer)
        await AddResult.gks_place.set()
    else:
        await message.answer(
            text="Вы ввели неверное чилсо. Введите число от 1 до 16"
        )
        await message.answer(
            text="Какое место заняла команда Прокат?"
        )
        await AddResult.prokat_place.set()
