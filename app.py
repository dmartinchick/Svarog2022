"""start app"""
import asyncio
from aiogram import executor

from loader import dp
import middlewares  # pylint: disable=unused-import
import filters      # pylint: disable=unused-import
import handlers     # pylint: disable=unused-import
from utils.db_api.db_comands import set_loging_update

from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    """ Запуск стартовой функции телеграмм бота
    """
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)

async def schedule_check(wait_for):
    """функция отправки запросов к ДБ"""
    while True:
        await asyncio.sleep(wait_for)

        set_loging_update()

if __name__ == '__main__':
    dp.loop.create_task(schedule_check(30))
    executor.start_polling(dp, on_startup=on_startup)
