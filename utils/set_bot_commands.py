"""Установки команд бота"""
from aiogram import types


async def set_default_commands(dp):
    """Устанавливает команды бота

    Args:
        dp ([type]): Диспатчер
    """
    await dp.bot.set_my_commands(
        [
            types.BotCommand("menu", "Показать главное меню"),
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("admin_panel", "Панель администратора")
        ]
    )
