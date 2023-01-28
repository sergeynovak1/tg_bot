from aiogram import Bot, Dispatcher, executor, types

from config import TOKEN
from keyboards import admin_menu


bot = Bot(TOKEN)
dp = Dispatcher(bot)


async def on_startup(_):
    pass


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.delete()
    await message.answer(text="Выберите пункт", reply_markup=admin_menu)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
