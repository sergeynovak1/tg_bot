import random
import time

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import config

from aiogram import Bot, Dispatcher, executor, types

bot = Bot(config.TOKEN)
dp = Dispatcher(bot)

BASE_SIMBOL = '◻️'
X_SIMBOL = '❌'
O_SIMBOL = '⭕️'


def get_inline_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=3)
    ikb.add(InlineKeyboardButton(field[0], callback_data='click_1'),
            InlineKeyboardButton(field[1], callback_data='click_2'),
            InlineKeyboardButton(field[2], callback_data='click_3'),
            InlineKeyboardButton(field[3], callback_data='click_4'),
            InlineKeyboardButton(field[4], callback_data='click_5'),
            InlineKeyboardButton(field[5], callback_data='click_6'),
            InlineKeyboardButton(field[6], callback_data='click_7'),
            InlineKeyboardButton(field[7], callback_data='click_8'),
            InlineKeyboardButton(field[8], callback_data='click_9'))

    return ikb


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    global field
    field = {0: BASE_SIMBOL, 1: BASE_SIMBOL, 2: BASE_SIMBOL,
             3: BASE_SIMBOL, 4: BASE_SIMBOL, 5: BASE_SIMBOL,
             6: BASE_SIMBOL, 7: BASE_SIMBOL, 8: BASE_SIMBOL}
    await message.delete()
    await message.answer(f'Твой ход', reply_markup=get_inline_keyboard())


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('click'))
async def click_button(callback: types.CallbackQuery) -> None:
    index = int(callback.data[-1]) - 1
    if field[index] == BASE_SIMBOL:
        field[index] = X_SIMBOL
        await callback.message.edit_text(text='Ход бота', reply_markup=get_inline_keyboard())
        bot_move()
        time.sleep(1)
        await callback.message.edit_text(text='Твой ход', reply_markup=get_inline_keyboard())
    else:
        await callback.message.edit_text(text='Нельзя сходить сюда', reply_markup=get_inline_keyboard())


def bot_move():
    move_list = [cell for cell in field if field[cell] == BASE_SIMBOL]
    if move_list:
        field[random.choice(move_list)] = O_SIMBOL


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True)
