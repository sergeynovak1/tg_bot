from aiogram import Bot, Dispatcher, executor, types

from config import TOKEN
from keyboards import admin_menu, admin_change_appointments


bot = Bot(TOKEN)
dp = Dispatcher(bot)


async def on_startup(_):
    pass


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.delete()
    await message.answer(text="Выберите пункт", reply_markup=admin_menu)


@dp.callback_query_handler(lambda callback: callback.data == 'appointments')
async def appointments(callback: types.CallbackQuery):
    ap = "Записи"
    await callback.message.edit_text(text=ap, reply_markup=admin_change_appointments)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
