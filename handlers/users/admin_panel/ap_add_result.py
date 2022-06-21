"""Пакет управления функцией администратора 'Добавить результат'"""
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards.inline.inline_admin_panel import admin_panel_keyboard, \
    ap_chcek_result, ap_event_keyboard

from loader import dp
from utils.db_api.db_comands import count_teams, get_event_name, \
    get_events_list, get_result_list, get_team_id, \
    get_team_name, set_results
from utils.misc.pillower_new import UpdateTables


class AddResult(StatesGroup):
    """Класс добавления результатов конкурсов

    Args:
        StatesGroup ([type]): [description]
    """
    event_name = State()
    prokat_place = State()
    emergency_place = State()
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
    belshina_place = State()
    iron_vikings_place = State()
    check_result = State()


@dp.callback_query_handler(text_contains="ap:add_result:save", state=AddResult.check_result)
async def save_results(call:types.CallbackQuery, state: FSMContext):
    """Сохранение результатов в БД

    Args:
        call (types.CallbackQuery): [description]
        state (FSMContext): [description]
    """
    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    results = await state.get_data()
    set_results(results)
    await state.finish()

    # Обновляем картинку с результатами
    # update_result_table(event_type=get_event_cup(results['event_id']))
    UpdateTables()

    markup = await admin_panel_keyboard()
    await call.message.answer(
        text="Результаты сохранены\n"\
            "Панель администратора",
        reply_markup=markup
    )


@dp.callback_query_handler(text_contains="ap:add_result:repeat", state=AddResult.check_result)
async def repeat_enter(call: types.CallbackQuery, state: FSMContext):
    """Повторный ввод результатов

    Args:
        call (types.CallbackQuery): [description]
        state (FSMContext): [description]
    """
    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    to_do = call.data.split(':')[1]

    await state.reset_state()

    markup = await ap_event_keyboard(
        events_list=get_events_list(),
        results_list=get_result_list(),
        to_do = to_do
    )
    await call.message.answer(
        text="Выберите конкурс результат которого вы хотите добавить",
        reply_markup=markup
    )
    await AddResult.event_name.set()


@dp.callback_query_handler(text_contains = "ap:add_result", state=None)
async def ap_add_result_start(call: types.CallbackQuery):
    """Функция вызова меню добавления результатов

    Args:
        call (types.CallbackQuery): [description]
    """

    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)
    to_do = call.data.split(':')[1]

    events_list = get_events_list()
    result_list = get_result_list()
    markup = await ap_event_keyboard(
        events_list,
        result_list,
        to_do = to_do
    )
    await call.message.answer(
        text="Выберите конкурс, результат которого хотите добавить",
        reply_markup=markup
    )
    await AddResult.event_name.set()


@dp.callback_query_handler(state = AddResult.event_name)
async def event_add_choosen(call: types.CallbackQuery, state: FSMContext):
    """добавляет выбраный конкурс в FSM Storege

    Args:
        call (types.CallbackQuery): данные callback
        state (FSMContext): [description]
    """
    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    to_do = call.data.split(':')[1]
    event = int(call.data.split(':')[3])

    result_list = get_result_list()
    if event in result_list:
        await call.message.answer(
            text="❗ Результат данного конкурса уже введен ❗"
        )
        event_list = get_events_list()
        markup = await ap_event_keyboard(
            event_list,
            result_list,
            to_do = to_do
        )
        await call.message.answer(
            text="Выберите конкурс результат которого вы хотите добавить",
            reply_markup=markup
        )
        await AddResult.event_name.set()
    else:
        await state.update_data(event_id = event)
        await call.message.answer(
            text="Для прекращения остановки ввода введите 'СТОП'\n"\
                "Какое место заняла команда Прокат?"
        )
        await AddResult.prokat_place.set()


@dp.message_handler(state=AddResult.prokat_place)
async def prokat_place_choosen(message: types.Message, state: FSMContext):
    """добавляет в FSM Storege место которое заняла команда Прокат

    Args:
        message (types.Message): [description]
        state (FSMContext): [description]
    """
    if message.text == "СТОП":
        await state.finish()
        markup = await admin_panel_keyboard()
        await message.answer(
            text="Панель администратора",
            reply_markup=markup
        )
    else:
        answer = int(message.text)
        team_id = get_team_id(name_en='prokat')
        count = count_teams()

        # Проверяем корректность ввода
        if answer > 0 and answer <= count:
            await state.update_data(prokat_place = {'team_id': team_id, 'place' : answer})
            await message.answer(
                text="Для прекращения остановки ввода введите 'СТОП'\n"\
                    "Какое место заняла команда EMERGENCY?")
            await AddResult.emergency_place.set()
        else:
            await message.answer(
                text=f"Вы ввели неверное чилсо. Введите число от 1 до {count}"
            )
            await message.answer(
                text="Для прекращения остановки ввода введите 'СТОП'\n"\
                    "Какое место заняла команда Прокат?"
            )
            await AddResult.prokat_place.set()


@dp.message_handler(state=AddResult.emergency_place)
async def emergency_place_choosen(message: types.Message, state: FSMContext):
    """добавляет в FSM Storege место которое заняла команда ГКС+Меттранс

    Args:
        message (types.Message): [description]
        state (FSMContext): [description]
    """
    if message.text == "СТОП":
        await state.finish()
        markup = await admin_panel_keyboard()
        await message.answer(
            text="Панель администратора",
            reply_markup=markup
        )
    else:
        answer = int(message.text)
        team_id = get_team_id(name_en='emergency')
        count = count_teams()

        # Проверяем корректность ввода
        if answer > 0 and answer <= count:
            await state.update_data(emergency_place = {'team_id': team_id, 'place' : answer})
            await message.answer(
                text="Для прекращения остановки ввода введите 'СТОП'\n"\
                    "Какое место заняла команда Сталь?")
            await AddResult.stal_place.set()
        else:
            await message.answer(
                text=f"Вы ввели неверное чилсо. Введите число от 1 до {count}"
            )
            await message.answer(
                text="Для прекращения остановки ввода введите 'СТОП'\n"\
                    "Какое место заняла команда EMERGENCY?"
            )
            await AddResult.emergency_place.set()


@dp.message_handler(state=AddResult.stal_place)
async def stal_place_choosen(message: types.Message, state: FSMContext):
    """добавляет в FSM Storege место которое заняла команда Сталь

    Args:
        message (types.Message): [description]
        state (FSMContext): [description]
    """
    if message.text == "СТОП":
        await state.finish()
        markup = await admin_panel_keyboard()
        await message.answer(
            text="Панель администратора",
            reply_markup=markup
        )
    else:
        answer = int(message.text)
        team_id = get_team_id(name_en='stal')
        count = count_teams()

        # Проверяем корректность ввода
        if answer > 0 and answer <= count:
            await state.update_data(stal_place = {'team_id': team_id, 'place' : answer})
            await message.answer(
                text="Для прекращения остановки ввода введите 'СТОП'\n"\
                    "Какое место заняла команда РАЗАМ?")
            await AddResult.razam_place.set()
        else:
            await message.answer(
                text=f"Вы ввели неверное чилсо. Введите число от 1 до {count}"
            )
            await message.answer(
                text="Для прекращения остановки ввода введите 'СТОП'\n"\
                    "Какое место заняла команда Сталь?"
            )
            await AddResult.stal_place.set()


@dp.message_handler(state=AddResult.razam_place)
async def razam_place_choosen(message: types.Message, state: FSMContext):
    """добавляет в FSM Storege место которое заняла команда РАЗАМ

    Args:
        message (types.Message): [description]
        state (FSMContext): [description]
    """
    if message.text == "СТОП":
        await state.finish()
        markup = await admin_panel_keyboard()
        await message.answer(
            text="Панель администратора",
            reply_markup=markup
        )
    else:
        answer = int(message.text)
        team_id = get_team_id(name_en='razam')
        count = count_teams()

        # Проверяем корректность ввода
        if answer > 0 and answer <= count:
            await state.update_data(razam_place = {'team_id': team_id, 'place' : answer})
            await message.answer(
                text="Для прекращения остановки ввода введите 'СТОП'\n"\
                    "Какое место заняла команда Белвторчермет?")
            await AddResult.belvtorchermet_place.set()
        else:
            await message.answer(
                text=f"Вы ввели неверное чилсо. Введите число от 1 до {count}"
            )
            await message.answer(
                text="Для прекращения остановки ввода введите 'СТОП'\n"\
                    "Какое место заняла команда РАЗАМ?"
            )
            await AddResult.razam_place.set()


@dp.message_handler(state=AddResult.belvtorchermet_place)
async def belvtorchermet_place_choosen(message: types.Message, state: FSMContext):
    """добавляет в FSM Storege место которое заняла команда Белвторчермет

    Args:
        message (types.Message): [description]
        state (FSMContext): [description]
    """
    if message.text == "СТОП":
        await state.finish()
        markup = await admin_panel_keyboard()
        await message.answer(
            text="Панель администратора",
            reply_markup=markup
        )
    else:
        answer = int(message.text)
        team_id = get_team_id(name_en='belvtorchermet')
        count = count_teams()

        # Проверяем корректность ввода
        if answer > 0 and answer <= count:
            await state.update_data(belvtorchermet_place = {'team_id': team_id, 'place' : answer})
            await message.answer(
                text="Для прекращения остановки ввода введите 'СТОП'\n"\
                    "Какое место заняла команда МПЗ?")
            await AddResult.mpz_place.set()
        else:
            await message.answer(
                text=f"Вы ввели неверное чилсо. Введите число от 1 до {count}"
            )
            await message.answer(
                text="Для прекращения остановки ввода введите 'СТОП'\n"\
                    "Какое место заняла команда Белвторчермет?"
            )
            await AddResult.belvtorchermet_place.set()


@dp.message_handler(state=AddResult.mpz_place)
async def mpz_place_choosen(message: types.Message, state: FSMContext):
    """добавляет в FSM Storege место которое заняла команда МПЗ

    Args:
        message (types.Message): [description]
        state (FSMContext): [description]
    """
    if message.text == "СТОП":
        await state.finish()
        markup = await admin_panel_keyboard()
        await message.answer(
            text="Панель администратора",
            reply_markup=markup
        )
    else:
        answer = int(message.text)
        team_id = get_team_id(name_en='mpz')
        count = count_teams()

        # Проверяем корректность ввода
        if answer > 0 and answer <= count:
            await state.update_data(mpz_place = {'team_id': team_id, 'place' : answer})
            await message.answer(
                text="Для прекращения остановки ввода введите 'СТОП'\n"\
                    "Какое место заняла команда ЗУбры?")
            await AddResult.zubry_place.set()
        else:
            await message.answer(
                text=f"Вы ввели неверное чилсо. Введите число от 1 до {count}"
            )
            await message.answer(
                text="Для прекращения остановки ввода введите 'СТОП'\n"\
                    "Какое место заняла команда МПЗ?"
            )
            await AddResult.mpz_place.set()


@dp.message_handler(state=AddResult.zubry_place)
async def zubry_place_choosen(message: types.Message, state: FSMContext):
    """добавляет в FSM Storege место которое заняла команда ЗУбры

    Args:
        message (types.Message): [description]
        state (FSMContext): [description]
    """
    if message.text == "СТОП":
        await state.finish()
        markup = await admin_panel_keyboard()
        await message.answer(
            text="Панель администратора",
            reply_markup=markup
        )
    else:
        answer = int(message.text)
        team_id = get_team_id(name_en='zubry')
        count = count_teams()

        # Проверяем корректность ввода
        if answer > 0 and answer <= count:
            await state.update_data(zubry_place = {'team_id': team_id, 'place' : answer})
            await message.answer(
                text="Для прекращения остановки ввода введите 'СТОП'\n"\
                    "Какое место заняла команда РМЗ?")
            await AddResult.rmz_place.set()
        else:
            await message.answer(
                text=f"Вы ввели неверное чилсо. Введите число от 1 до {count}"
            )
            await message.answer(
                text="Для прекращения остановки ввода введите 'СТОП'\n"\
                    "Какое место заняла команда ЗУбры?"
            )
            await AddResult.zubry_place.set()


@dp.message_handler(state=AddResult.rmz_place)
async def rmz_place_choosen(message: types.Message, state: FSMContext):
    """добавляет в FSM Storege место которое заняла команда РМЗ

    Args:
        message (types.Message): [description]
        state (FSMContext): [description]
    """
    if message.text == "СТОП":
        await state.finish()
        markup = await admin_panel_keyboard()
        await message.answer(
            text="Панель администратора",
            reply_markup=markup
        )
    else:
        answer = int(message.text)
        team_id = get_team_id(name_en='rmz')
        count = count_teams()

        # Проверяем корректность ввода
        if answer > 0 and answer <= count:
            await state.update_data(rmz_place = {'team_id': team_id, 'place' : answer})
            await message.answer(
                text="Для прекращения остановки ввода введите 'СТОП'\n"\
                    "Какое место заняла команда ByCord?")
            await AddResult.bycord_place.set()
        else:
            await message.answer(
                text=f"Вы ввели неверное чилсо. Введите число от 1 до {count}"
            )
            await message.answer(
                text="Для прекращения остановки ввода введите 'СТОП'\n"\
                    "Какое место заняла команда РМЗ?"
            )
            await AddResult.rmz_place.set()


@dp.message_handler(state=AddResult.bycord_place)
async def bycord_place_choosen(message: types.Message, state: FSMContext):
    """добавляет в FSM Storege место которое заняла команда ByCord

    Args:
        message (types.Message): [description]
        state (FSMContext): [description]
    """
    if message.text == "СТОП":
        await state.finish()
        markup = await admin_panel_keyboard()
        await message.answer(
            text="Панель администратора",
            reply_markup=markup
        )
    else:
        answer = int(message.text)
        team_id = get_team_id(name_en='bycord')
        count = count_teams()

        # Проверяем корректность ввода
        if answer > 0 and answer <= count:
            await state.update_data(bycord_place = {'team_id': team_id, 'place' : answer})
            await message.answer(
                text="Для прекращения остановки ввода введите 'СТОП'\n"\
                    "Какое место заняла команда Интеграл?")
            await AddResult.integral_place.set()
        else:
            await message.answer(
                text=f"Вы ввели неверное чилсо. Введите число от 1 до {count}"
            )
            await message.answer(
                text="Для прекращения остановки ввода введите 'СТОП'\n"\
                    "Какое место заняла команда ByCord?"
            )
            await AddResult.bycord_place.set()


@dp.message_handler(state=AddResult.integral_place)
async def integral_place_choosen(message: types.Message, state: FSMContext):
    """добавляет в FSM Storege место которое заняла команда Интеграл

    Args:
        message (types.Message): [description]
        state (FSMContext): [description]
    """
    if message.text == "СТОП":
        await state.finish()
        markup = await admin_panel_keyboard()
        await message.answer(
            text="Панель администратора",
            reply_markup=markup
        )
    else:
        answer = int(message.text)
        team_id = get_team_id(name_en='integral')
        count = count_teams()

        # Проверяем корректность ввода
        if answer > 0 and answer <= count:
            await state.update_data(integral_place = {'team_id': team_id, 'place' : answer})
            await message.answer(
                text="Для прекращения остановки ввода введите 'СТОП'\n"\
                    "Какое место заняла команда МЗКТ?")
            await AddResult.mzkt_place.set()
        else:
            await message.answer(
                text=f"Вы ввели неверное чилсо. Введите число от 1 до {count}"
            )
            await message.answer(
                text="Для прекращения остановки ввода введите 'СТОП'\n"\
                    "Какое место заняла команда Интеграл?"
            )
            await AddResult.integral_place.set()


@dp.message_handler(state=AddResult.mzkt_place)
async def mzkt_place_choosen(message: types.Message, state: FSMContext):
    """добавляет в FSM Storege место которое заняла команда МЗКТ

    Args:
        message (types.Message): [description]
        state (FSMContext): [description]
    """
    if message.text == "СТОП":
        await state.finish()
        markup = await admin_panel_keyboard()
        await message.answer(
            text="Панель администратора",
            reply_markup=markup
        )
    else:
        answer = int(message.text)
        team_id = get_team_id(name_en='mzkt')
        count = count_teams()

        # Проверяем корректность ввода
        if answer > 0 and answer <= count:
            await state.update_data(mzkt_place = {'team_id': team_id, 'place' : answer})
            await message.answer(
                text="Для прекращения остановки ввода введите 'СТОП'\n"\
                    "Какое место заняла команда МАЗ?")
            await AddResult.maz_place.set()
        else:
            await message.answer(
                text=f"Вы ввели неверное чилсо. Введите число от 1 до {count}"
            )
            await message.answer(
                text="Для прекращения остановки ввода введите 'СТОП'\n"\
                    "Какое место заняла команда МЗКТ?"
            )
            await AddResult.mzkt_place.set()

@dp.message_handler(state=AddResult.maz_place)
async def maz_place_choosen(message: types.Message, state: FSMContext):
    """добавляет в FSM Storege место которое заняла команда МАЗ

    Args:
        message (types.Message): [description]
        state (FSMContext): [description]
    """
    if message.text == "СТОП":
        await state.finish()
        markup = await admin_panel_keyboard()
        await message.answer(
            text="Панель администратора",
            reply_markup=markup
        )
    else:
        answer = int(message.text)
        team_id = get_team_id(name_en='maz')
        count = count_teams()

        # Проверяем корректность ввода
        if answer > 0 and answer <= count:
            await state.update_data(maz_place = {'team_id': team_id, 'place' : answer})
            await message.answer(
                text="Для прекращения остановки ввода введите 'СТОП'\n"\
                    "Какое место заняла команда Белшина?")
            await AddResult.belshina_place.set()
        else:
            await message.answer(
                text=f"Вы ввели неверное чилсо. Введите число от 1 до {count}"
            )
            await message.answer(
                text="Для прекращения остановки ввода введите 'СТОП'\n"\
                    "Какое место заняла команда МАЗ?"
            )
            await AddResult.maz_place.set()

@dp.message_handler(state=AddResult.belshina_place)
async def belshina_place_choosen(message: types.Message, state: FSMContext):
    """добавляет в FSM Storege место которое заняла команда МогилевЛифтМаш

    Args:
        message (types.Message): [description]
        state (FSMContext): [description]
    """
    if message.text == "СТОП":
        await state.finish()
        markup = await admin_panel_keyboard()
        await message.answer(
            text="Панель администратора",
            reply_markup=markup
        )
    else:
        answer = int(message.text)
        team_id = get_team_id(name_en='belshina')
        count = count_teams()

        # Проверяем корректность ввода
        if answer > 0 and answer <= count:
            await state.update_data(belshina_place = {'team_id': team_id, 'place' : answer})
            await message.answer(
                text="Для прекращения остановки ввода введите 'СТОП'\n"\
                    "Какое место заняла команда IRON VIKINGS?")
            await AddResult.iron_vikings_place.set()
        else:
            await message.answer(
                text=f"Вы ввели неверное чилсо. Введите число от 1 до {count}"
            )
            await message.answer(
                text="Для прекращения остановки ввода введите 'СТОП'\n"\
                    "Какое место заняла команда Белшина?"
            )
            await AddResult.belshina_place.set()


@dp.message_handler(state=AddResult.iron_vikings_place)
async def iron_vikings_place_choosen(message: types.Message, state: FSMContext):
    """добавляет в FSM Storege место которое заняла команда ММЗ

    Args:
        message (types.Message): [description]
        state (FSMContext): [description]
    """
    if message.text == "СТОП":
        await state.finish()
        markup = await admin_panel_keyboard()
        await message.answer(
            text="Панель администратора",
            reply_markup=markup
        )
    else:
        answer = int(message.text)
        team_id = get_team_id(name_en='iron_vikings')
        count = count_teams()

        # Проверяем корректность ввода
        if answer > 0 and answer <= count:
            await state.update_data(iron_vikings_place = {'team_id': team_id, 'place' : answer})
            results = await state.get_data()
            results_text = make_text_result(results)
            markup = await ap_chcek_result(to_do="add_result")
            await message.answer(
                text=results_text,
                reply_markup=markup
            )
        else:
            await message.answer(
                text=f"Вы ввели неверное чилсо. Введите число от 1 до {count}")
            await message.answer(
                text="Для прекращения остановки ввода введите 'СТОП'\n"\
                    "Какое место заняла команда IRON_VIKINGS?")
            await AddResult.iron_vikings_place.set()
        await AddResult.check_result.set()


def make_text_result(dic) -> str:
    """Формирует текст для проверки результатов

    Args:
        dic ([type]): Словарь из FSMcontex

    Returns:
        str: текст для проверки результатов
    TODO: Профести рефакторинг
    """
    event_id  = dic['event_id']
    event_name = get_event_name(event_id)
    rlist = list(dic.items())
    result_list = rlist[1:]
    text_result = f"Конкрс - {event_name}\n"
    for item in result_list:
        team_name = get_team_name(item[1]['team_id'])
        text_result = text_result + f"{team_name} - {item[1]['place']}\n"
    return text_result
