"""Пакет управления функцией администратора 'Экстренное сообщение'
TODO: Оценить необходимость данной функции"""

import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import dp

class EmergencyMessage(StatesGroup):
    """Класс отправки экстренных сообщений"""
    text_message = State()
    selecting_destinations = State()


@dp.callback_query_handler(text_contains="emergency_message", state=None)
async def ap_emergency_message(call: types.CallbackQuery):
    """Функция вызова меню отправки экстренных сообщений

    Args:
        call (types.CallbackQuery): [description]
    """

    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    await call.message.answer(
        text="Введите сообщение которое должно быть отправленно"
    )


@dp.message_handler(state=EmergencyMessage.text_message)
async def message_entry(message: types.Message, state: FSMContext):
    """ДОбавляет введенное сообщение в FSMContex

    Args:
        message (types.Message): _description_
        state (FSMContext): _description_
    TODO: добавить клавитуру с выбором группы получателей
    """
    await state.update_data(
        {'message_text' : message.text}
    )
    await message.answer(
        text="Выбирите группу людей, которая должна получить данное сообщение"
    )
    await EmergencyMessage.selecting_destinations.set()


@dp.callback_query_handler(
    text_contains = "ap:emergency_message",
    state=EmergencyMessage.selecting_destinations
)
async def selecting_destinations_choice(call: types.CallbackQuery, state: FSMContext):
    """Добовляет группу людей, кому должн быть направленно сообщение

    Args:
        call (types.CallbackQuery): _description_
        state (FSMContext): _description_
    TODO: релизовать функцию
    """
    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    pass
