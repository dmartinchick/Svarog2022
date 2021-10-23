"""Хэндлеры управления главным меню"""
from datetime import datetime, timedelta
import logging

from aiogram import types
#from aiogram.types.callback_query import CallbackQuery
#from aiogram.types.message import Message
#from aiogram.dispatcher.filters import Command

from utils.db_api.db_comands import get_date_start, get_date_end, get_full_shedule
from utils.db_api.db_comands import get_what_next, get_what_now

from handlers.users.subscriptions_menu import subscriptions_categories

#Загрузка клавиатур
from keyboards.inline.inline_main_menu import inkb_main_menu
from keyboards.inline.result_menu import inkb_result_menu
from keyboards.inline.contests_menu import inkb_contests_menu
# from keyboards.inline.subscriptions_menu import inkb_subscriptions_menu

from loader import dp
from data import config

@dp.message_handler(commands=['Меню', 'menu'], commands_prefix = ['⠀','/'])
async def show_main_menu(message: types.Message):
    """Отправляет пользователю сообщение с клавиатурой главного меню

    Args:
        message (types.Message): [description]
    """
    await message.answer(text="Главное меню", reply_markup=inkb_main_menu)


@dp.callback_query_handler(text_contains='back')
async def back_main_menu(call: types.CallbackQuery):
    """Возвращает пользователя в главное меню
    """
    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info(f"{callback_data=}")

    await call.message.answer(text="Главное меню", reply_markup=inkb_main_menu)

@dp.callback_query_handler(text_contains="main:what_now")
async def show_what_now(call: types.CallbackQuery):
    """Отправляет пользователю текущие события
    TODO: заменить tdate
    """

    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info(f"{callback_data=}")
    # текущее время и дата
    # tdate = datetime.now() + timedelta(hours=config.DELTA)
    tdate = datetime(2021, 7, 18, 19, 29) + timedelta(hours=config.DELTA)
    dt_start = get_date_start()
    dt_end = get_date_end()

    # Проверка начался ли фестиваль
    if tdate < dt_start:
        await call.message.answer(
            text="😁 Фестиваль еще не начался, \nЗагляни сюда 18 июня!"
            )
    elif tdate > dt_end:
        await call.message.answer(
            text="☹ К сожелению, фестиваль уже прошел.\nУвидимся в следующем году! 😁"
            )
    else:
        await call.message.answer(
            text='🤓 Сейча проходит 🤓'
            )
        # обращение к базе данных и получение данных
        events_list = get_what_now(tdate)
        # проверка есть ли меропириятия сейчас, если нет отправляет сообщение
        if len(events_list) == 0:
            await call.message.answer(
                text="К сожелению сейчас ничего не происходит.\n"
                "Можешь посмотреть ближайшие события нажав на кнокпу"
                # TODO: Доваить клавиатуру с кноппкой what_next
            )
        else:
            for event in events_list:
                # парсинг данных
                event_name = event['name']
                time_end = event['event_time_end'].strftime('%H:%M')
                # отправка сообщения с информацией о конкурсе
                await call.message.answer(
                    text=f"Саейчас проходит конкурс '{event_name}'\n"
                    f"Он закончиться в {time_end}"
                    )


@dp.callback_query_handler(text_contains="main:what_next")
async def show_what_next(call: types.CallbackQuery):
    """Возвращает пользователю ближайшее событие
    TODO: реализовать функцию show_what_next. добавить обратный отсчет?
    TODO: заменить tdate
    """
    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info(f"{callback_data=}")
    # получение текущей даты и времени, а так же даты и времени окончания фестиваля
    # tdate = datetime.now() + timedelta(hours=config.DELTA)
    tdate = datetime(2021, 7, 18, 19, 29) + timedelta(hours=config.DELTA)
    dt_end = get_date_end()
    # проверка не закончился ли фестиваль
    if tdate >= dt_end:
        await call.message.answer(
            text="☹ К сожелению, фестиваль уже прошел.\nУвидимся в следующем году! 😁"
            )
    else:
        # обращение к БД и получение ближайших мероприятий
        events_list = get_what_next(tdate)
        await call.message.answer("В скором времени состоится")
        # запуск цикла обработки текущих событий
        for event in events_list:
            await call.message.answer(
                                    f"'{event['name']}'\n"
                                    f"Конкурс начнется "
                                    f"{event['event_time_start'].strftime('%d.%m')} "
                                    f"в {event['event_time_start'].strftime('%H:%M')}")


@dp.callback_query_handler(text_contains="main:full_schedule")
async def show_full_schedule(call: types.CallbackQuery):
    """Возвращает пользователю полное расписание
    """
    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info(f"{callback_data=}")
    full_schedule = get_full_shedule()
    await call.message.answer("Вот полное расписание")
    for event in full_schedule:
        await call.message.answer(f"{event['name']}"
                                f"\nНачало:{event['time_start'].strftime('%d.%m %H:%M')}"
                                f"\nКонец:{event['time_end'].strftime('%d.%m %H:%M')}\n\n")


@dp.callback_query_handler(text_contains="main:results")
async def show_results_menu(call: types.CallbackQuery):
    """Возвращает пользователю таблицы результатов
    """

    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info(f"{callback_data=}")
    await call.message.answer("Выбери интересующие тебя результаты", reply_markup=inkb_result_menu)


@dp.callback_query_handler(text_contains="main:contests")
async def show_contests_menu(call: types.CallbackQuery):
    """Возвращает пользователю меню конкурсов
    """
    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info(f"{callback_data=}")
    await call.message.answer("Выбирите интересующий вас конкурс", reply_markup=inkb_contests_menu)


@dp.callback_query_handler(text_contains="main:subscriptions")
async def show_subscriptions_menu(call: types.CallbackQuery):
    """Возвращает пользователю меню подписок
    """
    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info(f"{callback_data=}")
    await subscriptions_categories(call)

@dp.callback_query_handler(text_contains="main:map")
async def show_map(call: types.CallbackQuery):
    """Возвращает пользователю кеарту фестиваля
    TODO: реализовать отправку картинки с картой фестиваля
    """
    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info(f"{callback_data=}")
    await call.message.answer("Вот карта фестиваля")


@dp.callback_query_handler(text_contains="main:share")
async def show_share(call: types.CallbackQuery):
    """Возвращает пользователю QR-код со сылкой на этот телеграм бот
    TODO: реализовать отправку картинки с QR-кодом
    """
    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info(f"{callback_data=}")
    await call.message.answer("Вот ссылка на телеграмм бота")


@dp.callback_query_handler(text_contains="main:about")
async def show_about(call: types.CallbackQuery):
    """Возвращает пользователю документ с положением фестиваля
    TODO: реализовать отправку файла с положением фестиваля
    """
    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info(f"{callback_data=}")
    await call.message.answer("Положение туристического фестиваля Свароог2022")
