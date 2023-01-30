from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import TOKEN
from keyboards import admin_menu, client_menu, admin_change_dates
from database import create_db, create_user, get_role, create_date
from main2 import get_date

bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Date(StatesGroup):
    date = State()
    time = State()


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


@dp.callback_query_handler(lambda callback_query: callback_query.data == "appointments")
async def list_dates(callback: types.CallbackQuery):
    dates = f'Тут будут даты'
    await callback.message.edit_text(text=dates, reply_markup=admin_change_dates())


@dp.callback_query_handler(lambda callback_query: callback_query.data == "add_date")
async def list_dates(callback: types.CallbackQuery):
    await Date.date.set()
    await callback.message.edit_text(text='Добавление даты\n\nНапишите дату в виде дд.мм')


@dp.message_handler(state=Date.date)
async def process_date_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text

    await Date.next()
    await message.reply("Напишите время чч:мм-чч:мм")

'''# Проверяем возраст
@dp.message_handler(lambda message: not message.text.isdigit(), state=Form.age)
async def process_age_invalid(message: types.Message):
    return await message.reply("Напиши возраст или напиши /cancel")'''


@dp.message_handler(state=Date.time)
async def process_date_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['time'] = message.text
    await state.finish()
    date = get_date(data['date'])
    create_date(date, data['time'])
    await bot.send_message(message.from_user.id, text="Свободные даты добавлены", reply_markup=admin_menu())




if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
