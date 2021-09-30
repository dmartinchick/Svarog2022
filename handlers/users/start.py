from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types.user import User
from keyboards.default.start_menu import start_menu_btn
from loader import dp
from utils.db_api.sqlighter import SQL


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):

    message_user = User.get_current()['id']
    rq = SQL.get_users()
    users_li = []
    for i in rq:
        users_li.append(i[0])
    if message_user in users_li:
        pass
    else:
        SQL.set_user(message_user)


    await message.answer(f"Привет ✋, {message.from_user.full_name}!\n\n"
                        "❗ Я телеграм бот туристического фестиваля Сварог2022\n"
                        "❗ Я подскажу какие мероприяти проходят прямо сейчас, а какие вот-вот начнуться.\n"
                        "❗ Раскажу о правилах конкурсов, и их результатах\n"
                        "❗ Отправлю напоминание, что бы ты мог следить за интересующими тебя конкурсами и командами")
    await message.answer("Для перехода к меню нажмите кнопку ниже 👇 или введите Меню", reply_markup=start_menu_btn)
