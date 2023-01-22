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
wait_user = []
game = {}
game_now = []
game_bot = {}


def get_menu_inline_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    ikb.add(InlineKeyboardButton('Игра с ботом', callback_data='bot'))
    ikb.add(InlineKeyboardButton('Игра с человеком', callback_data='user'))

    return ikb


def get_game_inline_keyboard(user_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=3)
    ikb.add(InlineKeyboardButton(game_bot[user_id][0], callback_data='click_1'),
            InlineKeyboardButton(game_bot[user_id][1], callback_data='click_2'),
            InlineKeyboardButton(game_bot[user_id][2], callback_data='click_3'),
            InlineKeyboardButton(game_bot[user_id][3], callback_data='click_4'),
            InlineKeyboardButton(game_bot[user_id][4], callback_data='click_5'),
            InlineKeyboardButton(game_bot[user_id][5], callback_data='click_6'),
            InlineKeyboardButton(game_bot[user_id][6], callback_data='click_7'),
            InlineKeyboardButton(game_bot[user_id][7], callback_data='click_8'),
            InlineKeyboardButton(game_bot[user_id][8], callback_data='click_9'))

    return ikb


@dp.message_handler(commands=['start'])
async def menu(message: types.Message) -> None:
    try:
        if message.text[0] == '/':
            await message.delete()
    except:
        pass
    await bot.send_message(message.from_user.id, text=f'Выберите режим игры.', reply_markup=get_menu_inline_keyboard())


@dp.callback_query_handler(lambda c: c.data.startswith('bot'))
async def bot_game(message: types.Message) -> None:
    global field, game_bot
    field = {cell: BASE_SIMBOL for cell in range(9)}
    game_bot[message.from_user.id] = field
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, text=f'Твой ход.', reply_markup=get_game_inline_keyboard(message.from_user.id))


def start_field():
    global field
    field = {cell: BASE_SIMBOL for cell in range(9)}


@dp.callback_query_handler(lambda c: c.data.startswith('user'))
async def bot_game(message: types.Message) -> None:
    global wait_user
    if message.from_user.id not in game:
        if message.from_user.id not in wait_user:
            wait_user.append(message.from_user.id)
        if len(wait_user) == 1:
            await bot.delete_message(message.from_user.id, message.message.message_id)
            global wait_user_id, wait_message
            wait_message = await bot.send_message(message.from_user.id, text=f'Ожидаем соперника.')
            wait_user_id = message.from_user.id
        elif len(wait_user) == 2:
            game[wait_user[0]] = wait_user[1]
            game[wait_user[1]] = wait_user[0]
            game_now.append(wait_user)
            wait_user = []
            await start_game(message)


async def start_game(message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.delete_message(wait_user_id, wait_message.message_id)
    await bot.send_message(message.from_user.id, text=f'Соперник найден.')
    await bot.send_message(game[message.from_user.id], text=f'Соперник найден')


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('click'))
async def click_field_button(callback: types.CallbackQuery) -> None:
    global game_bot
    index = int(callback.data[-1]) - 1
    if game_bot[callback.from_user.id][index] == BASE_SIMBOL:
        game_bot[callback.from_user.id][index] = X_SIMBOL
        if check_win(X_SIMBOL, callback.from_user.id) != '':
            await callback.message.edit_text(text=f'Ты выиграл!\n\nИтог игры:\n{check_win(X_SIMBOL, callback.from_user.id)}')
            await menu(callback)
        else:
            await callback.message.edit_text(text='Ход бота', reply_markup=get_game_inline_keyboard(callback.from_user.id))
            end_game = await bot_move(callback)
            time.sleep(1)
            if end_game:
                await callback.message.edit_text(text=f'Ничья!\n\nИтог игры:\n{end_game}')
                await menu(callback)
            else:
                if check_win(O_SIMBOL, callback.from_user.id):
                    await callback.message.edit_text(text=f'Бот выиграл!\n\nИтог игры:\n{check_win(O_SIMBOL, callback.from_user.id)}')
                    await menu(callback)
                else:
                    await callback.message.edit_text(text='Твой ход', reply_markup=get_game_inline_keyboard(callback.from_user.id))
    else:
        await callback.message.edit_text(text='Нельзя сходить сюда', reply_markup=get_game_inline_keyboard(callback.from_user.id))


async def bot_move(callback):
    move_list = [cell for cell in game_bot[callback.from_user.id] if game_bot[callback.from_user.id][cell] == BASE_SIMBOL]
    move_list_x = [cell for cell in game_bot[callback.from_user.id] if game_bot[callback.from_user.id][cell] == X_SIMBOL]
    move_list_o = [cell for cell in game_bot[callback.from_user.id] if game_bot[callback.from_user.id][cell] == O_SIMBOL]

    if move_list:
        if (4 in move_list) and ((0 in move_list_o and 8 in move_list_o) or (2 in move_list_o and 6 in move_list_o) or
                                 (1 in move_list_o and 7 in move_list_o) or (3 in move_list_o and 5 in move_list_o)):
            game_bot[callback.from_user.id][4] = O_SIMBOL
        elif (2 in move_list) and ((0 in move_list_o and 1 in move_list_o) or (5 in move_list_o and 8 in move_list_o) or
                                   (4 in move_list_o and 6 in move_list_o)):
            game_bot[callback.from_user.id][2] = O_SIMBOL
        elif (0 in move_list) and ((1 in move_list_o and 2 in move_list_o) or (3 in move_list_o and 6 in move_list_o) or
                                   (4 in move_list_o and 8 in move_list_o)):
            game_bot[callback.from_user.id][0] = O_SIMBOL
        elif (8 in move_list) and ((0 in move_list_o and 4 in move_list_o) or (2 in move_list_o and 5 in move_list_o) or
                                   (6 in move_list_o and 7 in move_list_o)):
            game_bot[callback.from_user.id][8] = O_SIMBOL
        elif (6 in move_list) and ((0 in move_list_o and 3 in move_list_o) or (2 in move_list_o and 4 in move_list_o) or
                                   (7 in move_list_o and 8 in move_list_o)):
            game_bot[callback.from_user.id][6] = O_SIMBOL
        elif (1 in move_list) and ((0 in move_list_o and 2 in move_list_o) or (4 in move_list_o and 7 in move_list_o)):
            game_bot[callback.from_user.id][1] = O_SIMBOL
        elif (3 in move_list) and ((0 in move_list_o and 6 in move_list_o) or (4 in move_list_o and 5 in move_list_o)):
            game_bot[callback.from_user.id][3] = O_SIMBOL
        elif (5 in move_list) and ((3 in move_list_o and 4 in move_list_o) or (2 in move_list_o and 8 in move_list_o)):
            game_bot[callback.from_user.id][5] = O_SIMBOL
        elif (7 in move_list) and ((1 in move_list_o and 4 in move_list_o) or (6 in move_list_o and 8 in move_list_o)):
            game_bot[callback.from_user.id][7] = O_SIMBOL
        elif (4 in move_list) and ((0 in move_list_x and 8 in move_list_x) or (2 in move_list_x and 6 in move_list_x) or
                                   (1 in move_list_x and 7 in move_list_x) or (3 in move_list_x and 5 in move_list_x)):
            game_bot[callback.from_user.id][4] = O_SIMBOL
        elif (2 in move_list) and ((0 in move_list_x and 1 in move_list_x) or (5 in move_list_x and 8 in move_list_x) or
                                   (4 in move_list_x and 6 in move_list_x)):
            game_bot[callback.from_user.id][2] = O_SIMBOL
        elif (0 in move_list) and ((1 in move_list_x and 2 in move_list_x) or (3 in move_list_x and 6 in move_list_x) or
                                   (4 in move_list_x and 8 in move_list_x)):
            game_bot[callback.from_user.id][0] = O_SIMBOL
        elif (8 in move_list) and ((0 in move_list_x and 4 in move_list_x) or (2 in move_list_x and 5 in move_list_x) or
                                   (6 in move_list_x and 7 in move_list_x)):
            game_bot[callback.from_user.id][8] = O_SIMBOL
        elif (6 in move_list) and ((0 in move_list_x and 3 in move_list_x) or (2 in move_list_x and 4 in move_list_x) or
                                   (7 in move_list_x and 8 in move_list_x)):
            game_bot[callback.from_user.id][6] = O_SIMBOL
        elif (1 in move_list) and ((0 in move_list_x and 2 in move_list_x) or (4 in move_list_x and 7 in move_list_x)):
            game_bot[callback.from_user.id][1] = O_SIMBOL
        elif (3 in move_list) and ((0 in move_list_x and 6 in move_list_x) or (4 in move_list_x and 5 in move_list_x)):
            game_bot[callback.from_user.id][3] = O_SIMBOL
        elif (5 in move_list) and ((3 in move_list_x and 4 in move_list_x) or (2 in move_list_x and 8 in move_list_x)):
            game_bot[callback.from_user.id][5] = O_SIMBOL
        elif (7 in move_list) and ((1 in move_list_x and 4 in move_list_x) or (6 in move_list_x and 8 in move_list_x)):
            game_bot[callback.from_user.id][7] = O_SIMBOL
        else:
            game_bot[callback.from_user.id][random.choice(move_list)] = O_SIMBOL
    else:
        return f'{game_bot[callback.from_user.id][0]}|{game_bot[callback.from_user.id][1]}|{game_bot[callback.from_user.id][2]}\n' \
               f'{game_bot[callback.from_user.id][3]}|{game_bot[callback.from_user.id][4]}|{game_bot[callback.from_user.id][5]}\n' \
               f'{game_bot[callback.from_user.id][6]}|{game_bot[callback.from_user.id][7]}|{game_bot[callback.from_user.id][8]}'


def check_win(symbol, user_id):
    if (game_bot[user_id][0] == game_bot[user_id][1] and game_bot[user_id][1] == game_bot[user_id][2] and game_bot[user_id][2] == symbol) or \
            (game_bot[user_id][3] == game_bot[user_id][4] and game_bot[user_id][4] == game_bot[user_id][5] and game_bot[user_id][5] == symbol) or \
            (game_bot[user_id][6] == game_bot[user_id][7] and game_bot[user_id][7] == game_bot[user_id][8] and game_bot[user_id][8] == symbol) or \
            (game_bot[user_id][0] == game_bot[user_id][3] and game_bot[user_id][3] == game_bot[user_id][6] and game_bot[user_id][6] == symbol) or \
            (game_bot[user_id][1] == game_bot[user_id][4] and game_bot[user_id][4] == game_bot[user_id][7] and game_bot[user_id][7] == symbol) or \
            (game_bot[user_id][2] == game_bot[user_id][5] and game_bot[user_id][5] == game_bot[user_id][8] and game_bot[user_id][8] == symbol) or \
            (game_bot[user_id][0] == game_bot[user_id][4] and game_bot[user_id][4] == game_bot[user_id][8] and game_bot[user_id][8] == symbol) or \
            (game_bot[user_id][2] == game_bot[user_id][4] and game_bot[user_id][4] == game_bot[user_id][6] and game_bot[user_id][6] == symbol):
        return f'{game_bot[user_id][0]}|{game_bot[user_id][1]}|{game_bot[user_id][2]}\n' \
               f'{game_bot[user_id][3]}|{game_bot[user_id][4]}|{game_bot[user_id][5]}\n' \
               f'{game_bot[user_id][6]}|{game_bot[user_id][7]}|{game_bot[user_id][8]}'
    return f''



if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True)
