"""Хэндлеры управления меню"""
from datetime import datetime, timedelta
import logging
from typing import Union

from aiogram import types

# Подгрузка команд для управления БД
from utils.db_api.db_comands import get_date_start, get_date_end, \
    get_event_info, get_full_shedule, \
        get_team_info, get_what_next, \
            get_what_now, set_sign_to_event, \
                set_sign_to_team, set_unsing_to_event, \
                    set_unsing_to_team

#Загрузка клавиатур
from keyboards.inline.inline_main_menu import event_keyboard, main_menu_keyboard, \
    result_keyboard, subscriptions_manager_keyboard, sm_item_keyboard, team_keyboard
from keyboards.inline.callback_datas import main_menu_cb

from loader import dp
from data import config

@dp.message_handler(commands=['Меню', 'menu'], commands_prefix = ['⠀','/'])
async def show_main_menu(
    message: Union[types.Message, types.CallbackQuery],
    **kwargs # pylint: disable=unused-argument
    ):

    """Отправляет пользователю сообщение с клавиатурой главного меню
    """

    markup = await main_menu_keyboard()

    if isinstance(message, types.Message):
        await message.answer(
            text="Главное меню",
            reply_markup=markup
        )
    elif isinstance(message, types.CallbackQuery):
        call = message
        await call.message.answer(
            text="Главное меню",
            reply_markup=markup
        )


async def show_what_now(
    call: types.CallbackQuery,
    **kwargs # pylint: disable=unused-argument
    ):

    """Отправляет пользователю текущие события
    TODO: заменить tdate
    TODO: Доваить клавиатуру с кноппкой what_next в ветку if len(events_list) == 0
    """

    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

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


async def show_what_next(
    call: types.CallbackQuery,
    **kwargs # pylint: disable=unused-argument
    ):

    """Возвращает пользователю ближайшее событие
    TODO: ????добавить обратный отсчет
    TODO: заменить tdate
    """

    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

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


async def show_full_schedule(
    call: types.CallbackQuery,
    **kwargs # pylint: disable=unused-argument
    ):

    """Возвращает пользователю полное расписание

    TODO: Офрмить более красивый текст
    """

    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    full_schedule = get_full_shedule()

    await call.message.answer("Вот полное расписание")

    for event in full_schedule:
        await call.message.answer(f"{event['name']}"
                                f"\nНачало:{event['time_start'].strftime('%d.%m %H:%M')}"
                                f"\nКонец:{event['time_end'].strftime('%d.%m %H:%M')}\n\n")


async def show_result_menu(
    call: types.CallbackQuery,
    category,
    **kwargs # pylint: disable=unused-argument
    ):

    """Возвращает пользователю меню результатов"""

    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    markup = await result_keyboard(category)

    await call.message.answer(
        text="Выберите интересующий вас кубок",
        reply_markup=markup
    )


async def show_festival_cup_result(
    call:types.CallbackQuery,
    **kwargs # pylint: disable=unused-argument
    ):

    """Возвращает пользователю результаты кубка Фестиваля

    Args:
        call (types.CallbackQuery): callback_data  пользователя
    """

    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    await call.message.answer(
        text="Вот результат кубка фестиваля"
    )


async def show_holding_cup_result(
    call: types.CallbackQuery,
    **kwargs # pylint: disable=unused-argument
    ):

    """Возвращает пользователю результаты кубка холдинга

    Args:
        call (types.CallbackQuery): callback_data пользователя
    """

    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    await call.message.answer(
        text="Вот результат кубка ходинга"
    )


async def show_tourism_cup_result(
    call: types.CallbackQuery,
    **kwargs # pylint: disable=unused-argument
    ):

    """Возвращает пользователю результаты кубка туризма

    Args:
        call (types.CallbackQuery): callback_data пользователя
    """

    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    await call.message.answer(
        text="Вот результат кубка туризма"
    )


async def show_sport_cup_result(
    call: types.CallbackQuery,
    **kwargs # pylint: disable=unused-argument
    ):

    """Возвращает пользователю результаты кубка спорта

    Args:
        call (types.CallbackQuery): callback_data пользователя
    """

    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    await call.message.answer(
        text="Вот результат кубка туризма"
    )


async def show_culture_cup_result(
    call: types.CallbackQuery,
    **kwargs # pylint: disable=unused-argument
    ):

    """Возвращает пользователю результаты кубка культуры

    Args:
        call (types.CallbackQuery): callback_data пользователя
    """

    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    await call.message.answer(
        text="Вот результат кубка культуры"
    )


async def show_event_menu(
    call: types.CallbackQuery,
    category,
    **kwargs # pylint: disable=unused-argument
    ):

    """Возвращает пользователю меню конкурсов

    Args:
        call (types.CallbackQuery): callback_data пользователя
        category ([type]): выбранная категория
    """

    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    markup = await event_keyboard(category)

    await call.message.answer(
        text="Выберите интересующий вас конкурс",
        reply_markup=markup
    )


async def show_team_menu(
    call: types.CallbackQuery,
    category,
    **kwargs # pylint: disable=unused-argument
    ):

    """Возвращает пользователю меню команд

    Args:
        call (types.CallbackQuery): callback_data пользователя
        category ([type]): выбранная категория
    """

    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    markup = await team_keyboard(category)

    await call.message.answer(
        text="Выберите интересующую вас команду",
        reply_markup=markup
    )


async def show_subscriptions_manager_menu(
    call: types.CallbackQuery,
    category,
    **kwargs # pylint: disable=unused-argument
    ):

    """Возвращает пользователю меню менеджера подписок

    Args:
        call (types.CallbackQuery): callbcak_data пользователя
        category ([type]): выбранная категория
    """

    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    markup = await subscriptions_manager_keyboard(category)

    await call.message.answer(
        text="Выберите какие подписки вы хоте ли бы настроить",
        reply_markup=markup
    )


async def show_subscriptions_manager_team(
    call: types.CallbackQuery,
    category,
    subcategory
    ):

    """Возвращает пользователю список команд на которые подписан/ не подписан пользователь

    Args:
        call (types.CallbackQuery): callback_data пользователя
        category ([type]): выбранная категория
        subcategory ([type]): выбранная подкатегория

    """

    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    user_id = call.from_user.id

    markup = await sm_item_keyboard(category, subcategory, user_id)

    await call.message.answer(
        text="Команды на которые вы уже подписаны помечены символом ✅\n"
            "Для того, что бы подписаться/отписаться от команды, "
            "нажмите на кнопку с её названием",
        reply_markup=markup
    )



async def show_subscriptions_manager_event(
    call: types.CallbackQuery,
    category,
    subcategory
    ):

    """Возвращает список конкурсов на которые подписан/ не подписан пользователь

    Args:
        call (types.CallbackQuery): callback_data пользователя
        category ([type]): выбранная категория
        subcategory ([type]): выбранная подкатегория

    """

    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    user_id = call.from_user.id
    markup = await sm_item_keyboard(category, subcategory, user_id)

    await call.message.answer(
        text="Конкурсы на которые вы уже подписаны помечены символом ✅\n"
            "Для того, что бы подписаться/отписаться от команды, "
            "нажмите на кнопку с её названием",
        reply_markup=markup
    )


async def show_map(
    call: types.CallbackQuery,
    **kwargs # pylint: disable=unused-argument
    ):

    """Возвращает пользователю карту фестиваля

    Args:
        call (types.CallbackQuery): callback_data пользователя

    TODO: реализовать отправку картинки с картой фестиваля
    """

    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    await call.message.answer("Вот карта фестиваля")


async def show_share(
    call: types.CallbackQuery,
    **kwargs # pylint: disable=unused-argument
    ):

    """Возвращает пользователю QR-код со сылкой на этот телеграм бот

    Args:
        call (types.CallbackQuery): callback_data пользователя

    TODO: реализовать отправку картинки с QR-кодом
    """

    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    await call.message.answer("Вот ссылка на телеграмм бота")


async def show_about(
    call: types.CallbackQuery,
    **kwargs # pylint: disable=unused-argument
    ):

    """Возвращает пользователю документ с положением фестиваля

    Args:
        call (types.CallbackQuery): callback_data пользователя

    TODO: реализовать отправку файла с положением фестиваля
    """

    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)

    await call.message.answer("Положение туристического фестиваля Свароог2022")


async def navigate_to_category(
    call: types.CallbackQuery,
    category,
    **kwargs # pylint: disable=unused-argument
    ):

    """Осуществляет навигацию по level 1

    Args:
        call (types.CallbackQuery): callback_data пользователя
        category ([type]): выбранная категория
    """
    categories = {
        "what_now" : show_what_now,
        "what_next" : show_what_next,
        "full_shedule" : show_full_schedule,
        "result" : show_result_menu,
        "event" : show_event_menu,
        "team" : show_team_menu,
        "sm" : show_subscriptions_manager_menu,
        "map" : show_map,
        "share" : show_share,
        "about" : show_about
    }

    curent_category_function = categories[category]

    await curent_category_function(
        call,
        category = category
    )


async def navigate_to_subcategory(
    call: types.CallbackQuery,
    category,
    subcategory,
    **kwargs # pylint: disable=unused-argument
    ):

    """осуществляет навигацию по level 2

    Args:
        call (types.CallbackQuery): callback_data пользователя
        category ([type]): выбранная категория
        subcategory ([type]): выбранная подкатегория
    """
    subcategories = {
        "festival_cup" : show_festival_cup_result,
        "holding_cup" : show_holding_cup_result,
        "sport_cup" : show_sport_cup_result,
        "tourism_cup" : show_tourism_cup_result,
        "culture_cup" : show_culture_cup_result,
        "sm_team" : show_subscriptions_manager_team,
        "sm_event" : show_subscriptions_manager_event
    }

    curent_subcategory_function = subcategories[subcategory]

    await curent_subcategory_function(
        call,
        category = category,
        subcategory = subcategory
    )


async def function_with_item(
    call: types.CallbackQuery,
    category:str,
    subcategory:str,
    action:str,
    item_id:str,
    **kwargs # pylint: disable=unused-argument
    ):

    """Осуществляет навигацию по работе с item

    Args:
        call (types.CallbackQuery): callback_data пользователя
        category (str): выбраная категория
        subcategory (str): выброная подкатегория
        action (str): необходимое действи на item
        item_id (str): id элемента

    """

    await call.answer(cache_time=360)
    callback_data = call.data
    logging.info("callback_data='%s'", callback_data)
    user_id = call.from_user.id

    actions = {
        "show":show_item_info,
        "subscribe" : subscribe_to_item,
        "unsubscribe" : unsubscribe_to_item
    }

    curent_action_function = actions[action]

    await curent_action_function(
        call,
        user_id,
        subcategory,
        item_id
    )


async def show_item_info(
    call : types.CallbackQuery,
    category:str,
    item_id:str,
    **kwargs # pylint: disable=unused-argument
    ):

    """Возвращет пользователю сообщение с информацией о конкурсе или команде

    Args:
        call (types.CallbackQuery): callback_data пользователя
        category (str): выбранная категория
        item_id (str): id конкурса или команды
    TODO: добавить кнопку "Подписаться" и "назад"
    """

    if category == "event":
        event_info = get_event_info(int(item_id))
        await call.message.answer(
            text=f"----{event_info['name']}---\n"
            f"{event_info['type']}\n\n"
            f"Коэфициент сложности: {event_info['coefficient']}\n\n"
            f"Состав представителей команд:\n{event_info['composition']}\n\n"
            f"Время старта конкурса:\n{event_info['time_start']}\n\n"
            f"Правила конкурса:\n{event_info['rule']}"
        )
    else:
        team_info = get_team_info(int(item_id))
        if team_info['holding'] is True:
            holding_text = "Команда входит в состав холдинга БМК"
        else:
            holding_text = "Команда не входит в состав холдинга БМК"
        await call.message.answer(
            text=f"---{team_info['name']}\n"
            f"{holding_text}"
        )


async def subscribe_to_item(
    call: types.CallbackQuery,
    user_id:int,
    subcategory:str,
    item_id:str,
    **kwargs # pylint: disable=unused-argument
    ):

    """Добавляет подписку

    Args:
        call (types.CallbackQuery): callback_data пользователя
        user_id (int): id пользователя
        category (str): выбранная категория
        item_id (str): id конкурса или команды
    """

    if subcategory == "sm_event":
        set_sign_to_event(int(user_id), int(item_id))
        await call.message.answer(
            text="Подписка добавлена"
        )
    elif subcategory == "sm_team":
        set_sign_to_team(int(user_id), int(item_id))
        await call.message.answer(
            text="Подписка добавлена"
        )
    else:
        await call.message.answer(
            text="Что то пошло не так"
        )


async def unsubscribe_to_item(
    call: types.CallbackQuery,
    user_id:int,
    subcategory:str,
    item_id:str,
    **kwargs # pylint: disable=unused-argument
    ):

    """Отменяет подписку

    Args:
        call (types.CallbackQuery): callback_data пользователя
        user_id (int): id пользователя
        category (str): выбранная категория
        item_id (str): id конкурса или команды
    """

    if subcategory == "sm_event":
        set_unsing_to_event(int(user_id), int(item_id))
        await call.message.answer(
            text="Подписка отменена"
        )
    elif subcategory == "sm_team":
        set_unsing_to_team(int(user_id), int(item_id))
        await call.message.answer(
            text="Подписка отменена"
        )
    else:
        await call.message.answer(
            text="Что то пошло не так"
        )


@dp.callback_query_handler(main_menu_cb.filter())
async def navigate_to_level(
    call: types.CallbackQuery,
    callback_data: dict
    ):

    """Осуществляет навигацию по level 0

    Args:
        call (types.CallbackQuery): callback_data пользователя
        callback_data (dict): словарь callback_data
    """

    curent_level = callback_data.get("level")
    category = callback_data.get("category")
    subcategory = callback_data.get("subcategory")
    action = callback_data.get("action")
    item_id = callback_data.get("item_id")

    levels = {
        "0" : show_main_menu,
        "1" : navigate_to_category,
        "2" : navigate_to_subcategory,
        "3" : function_with_item
    }

    curent_level_function = levels[curent_level]

    await curent_level_function(
        call,
        category = category,
        subcategory = subcategory,
        action = action,
        item_id = item_id
        )
