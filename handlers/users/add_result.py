"""Пакет управления функцией администратора 'Добавить результат'"""
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards.inline.inline_admin_panel import ap_event_keyboard

from loader import dp
from utils.db_api.db_comands import count_teams, get_team_id


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
    belvtorchermet_place = State()
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
    team_id = get_team_id(name_en='prokat')
    count = count_teams()

    # Проверяем корректность ввода
    if answer > 0 and answer <= count:
        await state.update_data(prokat_place = {'team_id': team_id, 'place' : answer})
        await message.answer("Какое место заняла команда ГКС+Меттранс?")
        await AddResult.gks_place.set()
    else:
        await message.answer(
            text=f"Вы ввели неверное чилсо. Введите число от 1 до {count}"
        )
        await message.answer(
            text="Какое место заняла команда Прокат?"
        )
        await AddResult.prokat_place.set()


@dp.message_handler(state=AddResult.gks_place)
async def gks_place_choosen(message: types.Message, state: FSMContext):
    """добавляет в FSM Storege место которое заняла команда ГКС+Меттранс

    Args:
        message (types.Message): [description]
        state (FSMContext): [description]
    """
    answer = int(message.text)
    team_id = get_team_id(name_en='gks')
    count = count_teams()

    # Проверяем корректность ввода
    if answer > 0 and answer <= count:
        await state.update_data(gks_place = {'team_id': team_id, 'place' : answer})
        await message.answer("Какое место заняла команда Сталь?")
        await AddResult.stal_place.set()
    else:
        await message.answer(
            text=f"Вы ввели неверное чилсо. Введите число от 1 до {count}"
        )
        await message.answer(
            text="Какое место заняла команда ГКС+Меттранс?"
        )
        await AddResult.gks_place.set()


@dp.message_handler(state=AddResult.stal_place)
async def stal_place_choosen(message: types.Message, state: FSMContext):
    """добавляет в FSM Storege место которое заняла команда Сталь

    Args:
        message (types.Message): [description]
        state (FSMContext): [description]
    """
    answer = int(message.text)
    team_id = get_team_id(name_en='stal')
    count = count_teams()

    # Проверяем корректность ввода
    if answer > 0 and answer <= count:
        await state.update_data(stal_place = {'team_id': team_id, 'place' : answer})
        await message.answer("Какое место заняла команда РАЗАМ?")
        await AddResult.razam_place.set()
    else:
        await message.answer(
            text=f"Вы ввели неверное чилсо. Введите число от 1 до {count}"
        )
        await message.answer(
            text="Какое место заняла команда Сталь?"
        )
        await AddResult.stal_place.set()


@dp.message_handler(state=AddResult.razam_place)
async def razam_place_choosen(message: types.Message, state: FSMContext):
    """добавляет в FSM Storege место которое заняла команда РАЗАМ

    Args:
        message (types.Message): [description]
        state (FSMContext): [description]
    """
    answer = int(message.text)
    team_id = get_team_id(name_en='razam')
    count = count_teams()

    # Проверяем корректность ввода
    if answer > 0 and answer <= count:
        await state.update_data(razam_place = {'team_id': team_id, 'place' : answer})
        await message.answer("Какое место заняла команда Белвторчермет?")
        await AddResult.belvtorchermet_place.set()
    else:
        await message.answer(
            text=f"Вы ввели неверное чилсо. Введите число от 1 до {count}"
        )
        await message.answer(
            text="Какое место заняла команда РАЗАМ?"
        )
        await AddResult.razam_place.set()


@dp.message_handler(state=AddResult.belvtorchermet_place)
async def belvtorchermet_place_choosen(message: types.Message, state: FSMContext):
    """добавляет в FSM Storege место которое заняла команда Белвторчермет

    Args:
        message (types.Message): [description]
        state (FSMContext): [description]
    """
    answer = int(message.text)
    team_id = get_team_id(name_en='belvtorchermet')
    count = count_teams()

    # Проверяем корректность ввода
    if answer > 0 and answer <= count:
        await state.update_data(belvtorchermet_place = {'team_id': team_id, 'place' : answer})
        await message.answer("Какое место заняла команда МПЗ?")
        await AddResult.mpz_place.set()
    else:
        await message.answer(
            text=f"Вы ввели неверное чилсо. Введите число от 1 до {count}"
        )
        await message.answer(
            text="Какое место заняла команда Белвторчермет?"
        )
        await AddResult.belvtorchermet_place.set()


@dp.message_handler(state=AddResult.mpz_place)
async def mpz_place_choosen(message: types.Message, state: FSMContext):
    """добавляет в FSM Storege место которое заняла команда МПЗ

    Args:
        message (types.Message): [description]
        state (FSMContext): [description]
    """
    answer = int(message.text)
    team_id = get_team_id(name_en='mpz')
    count = count_teams()

    # Проверяем корректность ввода
    if answer > 0 and answer <= count:
        await state.update_data(mpz_place = {'team_id': team_id, 'place' : answer})
        await message.answer("Какое место заняла команда ЗУбры?")
        await AddResult.zubry_place.set()
    else:
        await message.answer(
            text=f"Вы ввели неверное чилсо. Введите число от 1 до {count}"
        )
        await message.answer(
            text="Какое место заняла команда МПЗ?"
        )
        await AddResult.mpz_place.set()


@dp.message_handler(state=AddResult.zubry_place)
async def zubry_place_choosen(message: types.Message, state: FSMContext):
    """добавляет в FSM Storege место которое заняла команда ЗУбры

    Args:
        message (types.Message): [description]
        state (FSMContext): [description]
    """
    answer = int(message.text)
    team_id = get_team_id(name_en='zubry')
    count = count_teams()

    # Проверяем корректность ввода
    if answer > 0 and answer <= count:
        await state.update_data(zubry_place = {'team_id': team_id, 'place' : answer})
        await message.answer("Какое место заняла команда РМЗ?")
        await AddResult.rmz_place.set()
    else:
        await message.answer(
            text=f"Вы ввели неверное чилсо. Введите число от 1 до {count}"
        )
        await message.answer(
            text="Какое место заняла команда ЗУбры?"
        )
        await AddResult.zubry_place.set()


@dp.message_handler(state=AddResult.rmz_place)
async def rmz_place_choosen(message: types.Message, state: FSMContext):
    """добавляет в FSM Storege место которое заняла команда РМЗ

    Args:
        message (types.Message): [description]
        state (FSMContext): [description]
    """
    answer = int(message.text)
    team_id = get_team_id(name_en='rmz')
    count = count_teams()

    # Проверяем корректность ввода
    if answer > 0 and answer <= count:
        await state.update_data(rmz_place = {'team_id': team_id, 'place' : answer})
        await message.answer("Какое место заняла команда ByCord?")
        await AddResult.bycord_place.set()
    else:
        await message.answer(
            text=f"Вы ввели неверное чилсо. Введите число от 1 до {count}"
        )
        await message.answer(
            text="Какое место заняла команда РМЗ?"
        )
        await AddResult.rmz_place.set()


@dp.message_handler(state=AddResult.bycord_place)
async def bycord_place_choosen(message: types.Message, state: FSMContext):
    """добавляет в FSM Storege место которое заняла команда ByCord

    Args:
        message (types.Message): [description]
        state (FSMContext): [description]
    """
    answer = int(message.text)
    team_id = get_team_id(name_en='bycord')
    count = count_teams()

    # Проверяем корректность ввода
    if answer > 0 and answer <= count:
        await state.update_data(bycord_place = {'team_id': team_id, 'place' : answer})
        await message.answer("Какое место заняла команда Интеграл?")
        await AddResult.integral_place.set()
    else:
        await message.answer(
            text=f"Вы ввели неверное чилсо. Введите число от 1 до {count}"
        )
        await message.answer(
            text="Какое место заняла команда ByCord?"
        )
        await AddResult.bycord_place.set()


@dp.message_handler(state=AddResult.integral_place)
async def integral_place_choosen(message: types.Message, state: FSMContext):
    """добавляет в FSM Storege место которое заняла команда Интеграл

    Args:
        message (types.Message): [description]
        state (FSMContext): [description]
    """
    answer = int(message.text)
    team_id = get_team_id(name_en='integral')
    count = count_teams()

    # Проверяем корректность ввода
    if answer > 0 and answer <= count:
        await state.update_data(integral_place = {'team_id': team_id, 'place' : answer})
        await message.answer("Какое место заняла команда МЗКТ?")
        await AddResult.mzkt_place.set()
    else:
        await message.answer(
            text=f"Вы ввели неверное чилсо. Введите число от 1 до {count}"
        )
        await message.answer(
            text="Какое место заняла команда Интеграл?"
        )
        await AddResult.integral_place.set()


@dp.message_handler(state=AddResult.mzkt_place)
async def mzkt_place_choosen(message: types.Message, state: FSMContext):
    """добавляет в FSM Storege место которое заняла команда МЗКТ

    Args:
        message (types.Message): [description]
        state (FSMContext): [description]
    """
    answer = int(message.text)
    team_id = get_team_id(name_en='mzkt')
    count = count_teams()

    # Проверяем корректность ввода
    if answer > 0 and answer <= count:
        await state.update_data(mzkt_place = {'team_id': team_id, 'place' : answer})
        await message.answer("Какое место заняла команда МАЗ?")
        await AddResult.maz_place.set()
    else:
        await message.answer(
            text=f"Вы ввели неверное чилсо. Введите число от 1 до {count}"
        )
        await message.answer(
            text="Какое место заняла команда МЗКТ?"
        )
        await AddResult.mzkt_place.set()

@dp.message_handler(state=AddResult.maz_place)
async def maz_place_choosen(message: types.Message, state: FSMContext):
    """добавляет в FSM Storege место которое заняла команда МАЗ

    Args:
        message (types.Message): [description]
        state (FSMContext): [description]
    """
    answer = int(message.text)
    team_id = get_team_id(name_en='maz')
    count = count_teams()

    # Проверяем корректность ввода
    if answer > 0 and answer <= count:
        await state.update_data(maz_place = {'team_id': team_id, 'place' : answer})
        await message.answer("Какое место заняла команда МогилевЛифтМаш?")
        await AddResult.mogilevliftmash_place.set()
    else:
        await message.answer(
            text=f"Вы ввели неверное чилсо. Введите число от 1 до {count}"
        )
        await message.answer(
            text="Какое место заняла команда МАЗ?"
        )
        await AddResult.maz_place.set()

@dp.message_handler(state=AddResult.mogilevliftmash_place)
async def mogilevliftmash_place_choosen(message: types.Message, state: FSMContext):
    """добавляет в FSM Storege место которое заняла команда МогилевЛифтМаш

    Args:
        message (types.Message): [description]
        state (FSMContext): [description]
    """
    answer = int(message.text)
    team_id = get_team_id(name_en='mogilevliftmash')
    count = count_teams()

    # Проверяем корректность ввода
    if answer > 0 and answer <= count:
        await state.update_data(mogilevliftmash_place = {'team_id': team_id, 'place' : answer})
        await message.answer("Какое место заняла команда ММЗ?")
        await AddResult.mmz_place.set()
    else:
        await message.answer(
            text=f"Вы ввели неверное чилсо. Введите число от 1 до {count}"
        )
        await message.answer(
            text="Какое место заняла команда МогилевЛифтМаш?"
        )
        await AddResult.mogilevliftmash_place.set()


@dp.message_handler(state=AddResult.mmz_place)
async def mmz_place_choosen(message: types.Message, state: FSMContext):
    """добавляет в FSM Storege место которое заняла команда ММЗ

    Args:
        message (types.Message): [description]
        state (FSMContext): [description]
    """
    answer = int(message.text)
    team_id = get_team_id(name_en='mmz')
    count = count_teams()

    # Проверяем корректность ввода
    if answer > 0 and answer <= count:
        await state.update_data(mmz_place = {'team_id': team_id, 'place' : answer})
        await AddResult.save_results.set()
    else:
        await message.answer(
            text=f"Вы ввели неверное чилсо. Введите число от 1 до {count}"
        )
        await message.answer(
            text="Какое место заняла команда ММЗ?"
        )
        await AddResult.mmz_place.set()

@dp.message_handler(state=AddResult.save_results)
async def save_results_menu(message: types.Message, state: FSMContext):
    """Проверяет корректность ввода данных и сохраняет их при необходимости

    Args:
        message (types.Message): [description]
        state (FSMContext): [description]
    
    TODO: Реализвоать проверку данных и сохранение
    """
    results = await state.get_data()
    await message.answer(
        text=results
    )