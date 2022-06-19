"""start app"""
import asyncio
from aiogram import executor

from loader import dp
import middlewares  # pylint: disable=unused-import
import filters      # pylint: disable=unused-import
import handlers     # pylint: disable=unused-import
from utils.db_api.db_comands import delete_log_info, set_log_info
from utils.misc.other import get_tdate

from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    """ Запуск стартовой функции телеграмм бота
    """
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)

async def creat_log(wait_for):
    """pass"""
    while True:
        await asyncio.sleep(wait_for)
        t_date = get_tdate()
        set_log_info(t_date)

async def reset_log(wait_for):
    """pass"""
    while True:
        await asyncio.sleep(wait_for)
        delete_log_info()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(creat_log(30))
    loop.create_task(reset_log(100))
    executor.start_polling(dp, on_startup=on_startup)
