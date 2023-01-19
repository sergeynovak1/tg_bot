from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import config

from aiogram import Bot, Dispatcher, executor, types

bot = Bot(config.TOKEN)
dp = Dispatcher(bot)


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
    field = ['◻️']*9
    await message.answer(f'Твой ход',
                         reply_markup=get_inline_keyboard())


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('click'))
async def click(callback: types.CallbackQuery) -> None:
    global field
    index = int(callback.data[-1]) - 1
    field[index] = '❌'
    await callback.message.edit_text(text='Твой ход', reply_markup=get_inline_keyboard())


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True)