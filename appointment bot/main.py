from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove

from config import TOKEN
from keyboards import admin_menu, client_menu
from database import create_db, create_user, get_role

bot = Bot(TOKEN)
dp = Dispatcher(bot)


async def on_startup(_):
    create_db()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    create_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    await message.delete()
    if get_role(message.from_user.id) == 'client':
        await message.answer(text="Главное меню", reply_markup=client_menu())
    else:
        await message.answer(text="Выберите пункт", reply_markup=admin_menu())




if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
