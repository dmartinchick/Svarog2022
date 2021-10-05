from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types.user import User
from keyboards.default.start_menu import start_menu_btn
from loader import dp
from utils.db_api.db_comands import get_users_list, set_user


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):

    # Проверяем есть ли пользователь в БД. Если нет, то добавляем его в БД

    # Получаем id пользователя в Телеграмме
    message_user = message.from_user.id
    # Получаем список пользователей из БД
    users = get_users_list()
    if message_user not in users:
        set_user(message_user)
        


    await message.answer(f"Привет ✋, {message.from_user.full_name}!\n\n"
                        "❗ Я телеграм бот туристического фестиваля Сварог2022\n"
                        "❗ Я подскажу какие мероприяти проходят прямо сейчас, а какие вот-вот начнуться.\n"
                        "❗ Раскажу о правилах конкурсов, и их результатах\n"
                        "❗ Отправлю напоминание, что бы ты мог следить за интересующими тебя конкурсами и командами")
    await message.answer("Для перехода к меню нажмите кнопку ниже 👇 или введите Меню", reply_markup=start_menu_btn)
