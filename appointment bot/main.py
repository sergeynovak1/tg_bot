from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import TOKEN
from keyboards import admin_menu, client_menu, admin_change_dates, ikb_dates
from database import create_db, create_user, get_role, create_date, free_date, free_time
from main2 import get_db_date, get_data, get_date_from_db, get_time

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
    dates = [get_data(date) for date in free_date()]
    string = ''
    for date in dates:
        string += f"<b>{date}\t</b><em>\n"
        for time in free_time(get_db_date(date)):
            if time[3]:
                string += f"\t\t{get_time(time[2])}\t {time[3]}\n"
            else:
                string += f"\t\t{get_time(time[2])}\t CВОБОДНО\n"
        string += f"\n</em>"
    await callback.message.edit_text(text=string, reply_markup=admin_change_dates(), parse_mode="HTML")


@dp.callback_query_handler(lambda callback_query: callback_query.data == "add_date")
async def list_dates(callback: types.CallbackQuery):
    await Date.date.set()
    await callback.message.edit_text(text='Добавление даты\n\nНапишите дату в виде дд.мм')


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('ОК')
    await message.answer(text="Выберите пункт", reply_markup=admin_menu())


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
    date = get_db_date(data['date'])
    create_date(date, data['time'])
    await message.reply("Свободные даты добавлены")
    await message.answer(text="Выберите пункт", reply_markup=admin_menu())


@dp.callback_query_handler(lambda callback_query: callback_query.data == "del_date")
async def list_dates(callback: types.CallbackQuery):
    dates = [get_data(date) for date in free_date()]
    string = ''
    for date in dates:
        string += f"<b>{date}\t</b> /ddel{date[:2]}{date[3:]}\n<em>"
        for time in free_time(get_db_date(date)):
            if time[3]:
                string += f"\t\t{get_time(time[2])}\t {time[3]} /del{time[0]}\n"
            else:
                string += f"\t\t{get_time(time[2])}\t CВОБОДНО /del{time[0]}\n"
        string += f"\n</em>"
    await callback.message.edit_text(text=string, reply_markup=admin_change_dates(), parse_mode='HTML')








if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
