"""Хэндлеры управления админ панелью"""
import logging
from aiogram import types

from loader import dp
from data import config
from utils.db_api.db_comands import get_admin_list
"""Админ должен иметь возможность
    TODO: Отправлять экстренные сообщения
    TODO: добовлять результаты
    TODO: изменять расписание
"""




@dp.message_handler(commands="admin_panel")
async def show_admin_panel(message: types.Message):
    """Функция отображения панели адменистратора

    Args:
        message (types.Message): [description]
    """
    user_id = message.from_user.id
    # проверка имеется ли у пользователя админ права
    admins_list = get_admin_list()

    if user_id in admins_list:
        await message.answer(
            text="Панель администратора"
        )
    else:
        await message.answer(
            text="К сожалению у вас нет прав доступа. "\
                + "Для получения прав администатора - "\
                    + "обратитесь к главному судье фестиваля")

    pass
