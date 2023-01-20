import random
import time

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import config

from aiogram import Bot, Dispatcher, executor, types

bot = Bot(config.TOKEN)
dp = Dispatcher(bot)

BASE_SIMBOL = '◻'
X_SIMBOL = '❌'
O_SIMBOL = '⭕️'


def get_menu_inline_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    ikb.add(InlineKeyboardButton('Игра с ботом', callback_data='bot'))

    return ikb


def get_game_inline_keyboard() -> InlineKeyboardMarkup:
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
async def menu(message: types.Message) -> None:
    try:
        await message.delete()
    except:
        pass
    await bot.send_message(message.from_user.id, text=f'Выберите режим игры.', reply_markup=get_menu_inline_keyboard())


@dp.callback_query_handler(lambda c: c.data.startswith('bot'))
async def bot_game(message: types.Message) -> None:
    global field
    field = {0: BASE_SIMBOL, 1: BASE_SIMBOL, 2: BASE_SIMBOL,
             3: BASE_SIMBOL, 4: BASE_SIMBOL, 5: BASE_SIMBOL,
             6: BASE_SIMBOL, 7: BASE_SIMBOL, 8: BASE_SIMBOL}
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, text=f'Твой ход.', reply_markup=get_game_inline_keyboard())


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('click'))
async def click_field_button(callback: types.CallbackQuery) -> None:
    index = int(callback.data[-1]) - 1
    if field[index] == BASE_SIMBOL:
        field[index] = X_SIMBOL
        if check_win(X_SIMBOL):
            await callback.message.edit_text(text=f'Ты выиграл!\n\nИтог игры:\n{check_win(X_SIMBOL)}')
            await menu(callback)
        else:
            await callback.message.edit_text(text='Ход бота', reply_markup=get_game_inline_keyboard())
            bot_move()
            time.sleep(1)
            if check_win(O_SIMBOL):
                await callback.message.edit_text(text=f'Бот выиграл!\n\nИтог игры:\n{check_win(O_SIMBOL)}')
                await menu(callback)
            else:
                await callback.message.edit_text(text='Твой ход', reply_markup=get_game_inline_keyboard())
    else:
        await callback.message.edit_text(text='Нельзя сходить сюда', reply_markup=get_game_inline_keyboard())


def bot_move():
    move_list = [cell for cell in field if field[cell] == BASE_SIMBOL]
    move_list_x = [cell for cell in field if field[cell] == X_SIMBOL]
    if move_list:
        if (4 in move_list) and ((0 in move_list_x and 8 in move_list_x) or (2 in move_list_x and 6 in move_list_x) or (1 in move_list_x and 7 in move_list_x) or (3 in move_list_x and 5 in move_list_x)):
            field[4] = O_SIMBOL
        elif (1 in move_list) and ((0 in move_list_x and 2 in move_list_x) or (4 in move_list_x and 7 in move_list_x)):
            field[1] = O_SIMBOL
        elif (3 in move_list) and ((0 in move_list_x and 6 in move_list_x) or (4 in move_list_x and 5 in move_list_x)):
            field[3] = O_SIMBOL
        elif (5 in move_list) and ((3 in move_list_x and 4 in move_list_x) or (2 in move_list_x and 8 in move_list_x)):
            field[5] = O_SIMBOL
        elif (7 in move_list) and ((1 in move_list_x and 4 in move_list_x) or (6 in move_list_x and 8 in move_list_x)):
            field[7] = O_SIMBOL
        elif (2 in move_list) and ((0 in move_list_x and 1 in move_list_x) or (5 in move_list_x and 8 in move_list_x) or (4 in move_list_x and 6 in move_list_x)):
            field[2] = O_SIMBOL
        elif (0 in move_list) and ((1 in move_list_x and 2 in move_list_x) or (3 in move_list_x and 6 in move_list_x) or (4 in move_list_x and 8 in move_list_x)):
            field[0] = O_SIMBOL
        elif (8 in move_list) and ((0 in move_list_x and 4 in move_list_x) or (2 in move_list_x and 5 in move_list_x) or (6 in move_list_x and 7 in move_list_x)):
            field[8] = O_SIMBOL
        elif (6 in move_list) and ((0 in move_list_x and 3 in move_list_x) or (2 in move_list_x and 4 in move_list_x) or (7 in move_list_x and 8 in move_list_x)):
            field[6] = O_SIMBOL
        else:
            field[random.choice(move_list)] = O_SIMBOL


def check_win(symbol):
    if (field[0] == field[1] and field[1] == field[2]  and field[2] == symbol) or \
            (field[3] == field[4] and field[4] == field[5] and field[5] == symbol) or \
            (field[6] == field[7] and field[7] == field[8] and field[8] == symbol) or \
            (field[0] == field[3] and field[3] == field[6] and field[6] == symbol) or \
            (field[1] == field[4] and field[4] == field[7] and field[7] == symbol) or \
            (field[2] == field[5] and field[5] == field[8] and field[8] == symbol) or \
            (field[0] == field[4] and field[4] == field[8] and field[8] == symbol) or \
            (field[2] == field[4] and field[4] == field[6] and field[6] == symbol):
        return f'{field[0]}|{field[1]}|{field[2]}\n' \
               f'{field[3]}|{field[4]}|{field[5]}\n' \
               f'{field[6]}|{field[7]}|{field[8]}'
    return ''


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True)
