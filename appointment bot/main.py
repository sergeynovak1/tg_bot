import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

import datetime

from config import TOKEN
from keyboards import user_menu, client_menu, admin_change_dates, ikb_data, cancel, rkb_menu, ikb_confirm_action, \
    callback_date
from database import create_db, create_user, get_role, create_date, free_date, free_time, del_time, get_time_by_id, \
    del_date, all_date, all_time, get_appointment_by_date_time, make_appointment, get_name_by_id, get_app_by_name, \
    remove_appointment, app_info, id_in_date
from main2 import get_db_date, get_data, get_time, insert_appointment


bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Date(StatesGroup):
    date = State()
    time = State()


class Appoint(StatesGroup):
    phone = State()


async def on_startup(_):
    create_db()


def admin(func):
    async def wrapper(message):
        if get_role(message['from']['id']) != 'admin':
            return await message.reply("У вас нет прав на это")
        return await func(message)
    return wrapper


async def background_on_action() -> None:
    """background task which is created when user asked"""
    i = 0
    while True:
        i += 1
        await asyncio.sleep(3)
        print("Action!", i)


async def background_task_creator() -> None:
    """Creates background tasks"""
    asyncio.create_task(background_on_action())


@dp.message_handler(commands=['start', 'menu'])
async def cmd_start(message: types.Message):
    create_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    await message.delete()
    if get_role(message.from_user.id) == 'client':
        await message.answer(text="Главное меню", reply_markup=user_menu(message.from_user.id))
    else:
        for i in asyncio.all_tasks():
            print(i)
        if len(asyncio.all_tasks()) <= 3:
            await background_task_creator()
        await message.answer(text="Выберите пункт", reply_markup=user_menu(message.from_user.id))


@dp.callback_query_handler(lambda callback_query: callback_query.data == "menu")
async def list_dates(callback: types.CallbackQuery):
    if get_role(callback.from_user.id) == 'client':
        await callback.message.delete()
    else:
        await callback.message.edit_text(text="Выберите пункт", reply_markup=user_menu(callback.from_user.id))


@dp.callback_query_handler(lambda callback_query: callback_query.data == "appointments")
@admin
async def list_dates(callback: types.CallbackQuery):
    dates = [get_data(date) for date in all_date()]
    string = ''
    for date in dates:
        string += f"<b>{date}\t</b><em>\n"
        for time in all_time(get_db_date(date)):
            if time[3]:
                try:
                    string += f"\t\t{get_time(time[2])}\t @{get_name_by_id(time[3])}\n"
                except:
                    string += f"\t\t{get_time(time[2])}\t {time[3]}\n"
            else:
                string += f"\t\t{get_time(time[2])}\t CВОБОДНО\n"
        string += f"\n</em>"
    if not string:
        string = "<em>Нет актуальных записей</em>"
    await callback.message.edit_text(text=string, parse_mode="HTML")
    await bot.send_message(callback.from_user.id, text="Выберите пункт", reply_markup=user_menu(callback.from_user.id))


@dp.callback_query_handler(lambda callback_query: callback_query.data == "change_appointments")
@admin
async def change_appointments(callback: types.CallbackQuery):
    await callback.message.edit_text(text="Выберите пункт", reply_markup=admin_change_dates(), parse_mode="HTML")


@dp.callback_query_handler(lambda callback_query: callback_query.data == "add_date")
@admin
async def list_dates(callback: types.CallbackQuery):
    await Date.date.set()
    await callback.message.delete()
    await bot.send_message(callback.from_user.id, text='Добавление даты\n\nНапишите дату в виде дд.мм', reply_markup=cancel())


@dp.message_handler(commands=['cancel'], state='*')
async def cmd_cancel(message: types.Message, state: FSMContext):
    if state is None:
        return
    await state.finish()
    await message.reply("Добавление новых дат прервано")
    await bot.send_message(message.from_user.id, text="Выберите пункт", reply_markup=user_menu(message.from_user.id))


def check_date(date):
    if date[:2].isdigit() and date[3:].isdigit() and date[2] == '.':
        return True
    return False


@dp.message_handler(lambda message: not check_date(message.text), state=Date.date)
async def date_error(message: types.Message):
    await message.reply('<b>Неправильный формат даты</b>\n\nНапишите дату в виде дд.мм', parse_mode="HTML", reply_markup=cancel())


@dp.message_handler(state=Date.date)
async def process_date_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text
    await Date.next()
    await message.reply("Напишите время в виде чч:мм или промежуток чч:мм-чч:мм", reply_markup=cancel())


def check_time(time):
    if len(time) not in [5, 11]:
        return False
    time = time.split('-')
    for t in time:
        if not (t[:2].isdigit() and t[2] == ':' and t[3:].isdigit()):
            return False
    return True


@dp.message_handler(lambda message: not check_time(message.text), state=Date.time)
@admin
async def time_error(message: types.Message):
    await message.reply('<b>Неправильный формат времени</b>\n\nНапишите время в виде чч:мм или промежуток чч:мм-чч:мм', parse_mode="HTML", reply_markup=cancel())


@dp.message_handler(state=Date.time)
async def process_date_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['time'] = message.text
    await state.finish()
    date = get_db_date(data['date'])
    insert_appointment(date, data['time'])
    await message.reply("Свободные даты добавлены")
    await message.answer(text="Выберите пункт", reply_markup=user_menu(message.from_user.id))


@dp.callback_query_handler(lambda callback_query: callback_query.data == "change_date")
@admin
async def list_dates(callback: types.CallbackQuery):
    dates = [get_data(date) for date in all_date()]
    string = ''
    for date in dates:
        string += f"<b>{date}\t</b> /ddel{date[:2]}{date[3:]}\n<em>"
        for time in all_time(get_db_date(date)):
            if time[3]:
                try:
                    string += f"\t\t{get_time(time[2])}\t @{get_name_by_id(time[3])} /del{time[0]} /rem{time[0]}\n"
                except:
                    string += f"\t\t{get_time(time[2])}\t {time[3]} /del{time[0]} /rem{time[0]}\n"
            else:
                string += f"\t\t{get_time(time[2])}\t CВОБОДНО /del{time[0]}\n"
        string += f"\n</em>"
    if not string:
        string = "<em>Нет актуальных записей</em>"
    await callback.message.delete()
    await bot.send_message(callback.from_user.id, text=string, reply_markup=rkb_menu(), parse_mode='HTML')


@dp.message_handler(lambda message: message.text.startswith('/del'))
@admin
async def try_delet_time(message: types.Message):
    date_id = message.text[4:]
    date = get_data(get_time_by_id(date_id)[0])
    time = get_time(get_time_by_id(date_id)[1])
    await message.reply(text=f"Вы действительно хотите удалить запись <b>{date}</b> на {time}?",
                        reply_markup=ikb_confirm_action('del_time', date_id), parse_mode="HTML")


@dp.message_handler(lambda message: message.text.startswith('/ddel'))
@admin
async def try_delet_date(message: types.Message):
    date = f"{message.text[5:][:2]}.{message.text[5:][2:]}"
    await message.reply(text=f"Вы действительно хотите удалить все записи на <b>{date}</b>?",
                        reply_markup=ikb_confirm_action('del_date', date), parse_mode="HTML")


@dp.message_handler(lambda message: message.text.startswith('/rem'))
async def try_del_app(message: types.Message):
    date_id = message.text[4:]
    date = get_data(get_time_by_id(date_id)[0])
    time = get_time(get_time_by_id(date_id)[1])
    if get_role(message.from_user.id) == 'admin':
        text = f"Вы действительно хотите удалить запись клиента на <b>{date}</b> {time}?"
    else:
        text = f"Вы действительно хотите удалить запись на <b>{date}</b> {time}?"
    await message.delete()
    await message.answer(text=text, reply_markup=ikb_confirm_action('rem_app', date_id), parse_mode="HTML")


@dp.callback_query_handler(callback_date.filter())
async def cb_action(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'rem_app':
        date_id = callback_data['data']
        date = get_data(get_time_by_id(date_id)[0])
        time = get_time(get_time_by_id(date_id)[1])
        if get_role(callback.from_user.id) == 'admin':
            await callback.message.delete()
            await bot.send_message(callback.from_user.id, text=f"Запись клиента на <b>{date}</b>\t{time} удалена",
                                   reply_markup=rkb_menu(), parse_mode="HTML")
            try:
                app = app_info(date_id)
                await bot.send_message(app, text=f"Ваша запись на <b>{date}</b>\t{time} была удалена администратором", parse_mode="HTML")
            except:
                pass
            finally:
                remove_appointment(date_id)
        else:
            await callback.message.edit_text(text=f"Ваша запись на <b>{date}</b>\t{time} удалена", parse_mode="HTML")
    if get_role(callback.from_user.id) == 'admin':
        if callback_data['action'] == 'del_time':
            date_id = callback_data['data']
            date = get_data(get_time_by_id(date_id)[0])
            time = get_time(get_time_by_id(date_id)[1])
            await callback.message.delete()
            await bot.send_message(callback.from_user.id, text=f"Запись <b>{date}</b>\t{time} удалена",
                                   reply_markup=rkb_menu(), parse_mode="HTML")
            try:
                app = app_info(date_id)
                await bot.send_message(app, text=f"Ваша запись на <b>{date}</b>\t{time} была удалена администратором", parse_mode="HTML")
            except:
                pass
            finally:
                del_time(date_id)
        elif callback_data['action'] == 'del_date':
            date = callback_data['data']
            ids = [id[0] for id in id_in_date(get_db_date(date))]
            for date_id in ids:
                time = get_time(get_time_by_id(date_id)[1])
                try:
                    app = app_info(date_id)
                    await bot.send_message(app,
                                           text=f"Ваша запись на <b>{date}</b>\t{time} была удалена администратором",
                                           parse_mode="HTML")
                except:
                    pass
            del_date(date)
            await callback.message.delete()
            await bot.send_message(callback.from_user.id, text=f"Все записи на <b>{date}</b> удалены",
                                   reply_markup=rkb_menu(), parse_mode="HTML")
    elif callback_data['action'] == 'add_app':
        date_id = callback_data['data']
        user_id = callback.from_user.id
        make_appointment(user_id, date_id)
        date = get_data(get_time_by_id(date_id)[0])
        time = get_time(get_time_by_id(date_id)[1])
        await callback.message.edit_text(text=f"Вы записаны на <b>{date}</b> {time}", parse_mode="HTML")


@dp.message_handler(lambda message: message.text == 'Записаться на стрижку')
async def choose_date(message: types.Message):
    dates = [get_data(date) for date in free_date() if date >= datetime.date.today()]
    if dates:
        await message.reply(text=f"Выберите дату:", reply_markup=ikb_data('date', dates))
    else:
        await message.reply(text=f"<em>Нет актуальных дат</em>", reply_markup=user_menu(message.from_user.id), parse_mode='html')


@dp.callback_query_handler(lambda callback_query: callback_query.data == "make_appointments")
async def choose_date_admin(callback: types.CallbackQuery):
    dates = [get_data(date) for date in free_date() if date >= datetime.date.today()]
    if dates:
        ikb = ikb_data('date', dates).add(InlineKeyboardButton(text="Меню", callback_data="menu"))
        await callback.message.edit_text(text=f"Выберите дату:", reply_markup=ikb)
    else:
        await callback.message.edit_text(text=f"<em>Нет актуальных дат</em>", parse_mode='html')
        await bot.send_message(callback.from_user.id, text="Выберите пункт", reply_markup=user_menu(callback.from_user.id))


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("date"))
async def choose_time(callback: types.CallbackQuery):
    date = get_db_date(callback.data[4:])
    times = [get_time(time[0]) for time in free_time(date) if time[0] >= (datetime.datetime.now() - datetime.timedelta(hours=0, minutes=10)).time()]
    ikb = ikb_data(f"time{date}", times).add(InlineKeyboardButton(text="Назад", callback_data="make_appointments"))
    if times:
        await callback.message.edit_text(text=f"Выберите время:", reply_markup=ikb)
    else:
        await callback.message.edit_text(text=f"<em>К сожалению, на эту дату больше нет свободного времени</em>", reply_markup=ikb, parse_mode='html')


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("time"))
async def choose_time(callback: types.CallbackQuery, state: FSMContext):
    date = callback.data[4:14]
    time = callback.data[14:]
    date_id = get_appointment_by_date_time(date, time)[0]
    if get_role(callback.from_user.id) != 'admin':
        await callback.message.edit_text(text=f"Вы действительно хотите записаться на <b>{date[3:5]}.{date[:2]}</b> {time}?",
                            reply_markup=ikb_confirm_action('add_app', date_id), parse_mode="HTML")
    else:
        async with state.proxy() as data:
            data['date_id'] = date_id
        await Appoint.phone.set()
        await callback.message.delete()
        await bot.send_message(callback.from_user.id, text='Напишите номер телефона или @tg клиента',
                               reply_markup=cancel())


@dp.message_handler(state=Appoint.phone)
async def add_app_contact(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text
    await state.finish()
    make_appointment(data['phone'], data['date_id'])
    await message.reply("Запись добавлена")
    await bot.send_message(message.from_user.id, text="Выберите пункт", reply_markup=user_menu(message.from_user.id))


@dp.message_handler(lambda message: message.text == 'Мои записи')
async def my_appointments(message: types.Message):
    apps = get_app_by_name(message.from_user.id)
    string = ''
    for app in apps:
        date = get_data(app[1])
        time = get_time(app[2])
        string += f"\t\t<em><b>{date}\t</b> {time} /rem{app[0]}\n</em>"
    if not string:
        string = "<em>Нет актуальных записей</em>"
    else:
        string = "<em>Ваши записи:</em>\n" + string
    await message.reply(text=string, parse_mode="HTML")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
