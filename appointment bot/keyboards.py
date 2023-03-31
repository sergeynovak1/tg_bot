from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData

from database import get_role

callback_date = CallbackData('real_del_time', 'action', 'data')


def user_menu(user_id):
    if get_role(user_id) == 'admin':
        ikb = InlineKeyboardMarkup()
        ikb.add(
            InlineKeyboardButton(text="Настроить расписание", callback_data="change_appointments")).add(
            InlineKeyboardButton(text="Посмотреть записи", callback_data="appointments")).add(
            InlineKeyboardButton(text="Записать на стрижку", callback_data="make_appointments")).add(
            InlineKeyboardButton(text="Сделать рассылку", callback_data=" "))
    else:
        ikb = ReplyKeyboardMarkup(resize_keyboard=True)
        ikb.add(
            KeyboardButton(text="Записаться на стрижку")).add(
            KeyboardButton(text="Мои записи"))
    return ikb


def client_menu():
    ikb = ReplyKeyboardMarkup(resize_keyboard=True)
    ikb.add(
        KeyboardButton(text="Записаться на стрижку")).add(
        KeyboardButton(text="Мои записи"))
    return ikb


def menu():
    ikb = InlineKeyboardMarkup()
    ikb.add(InlineKeyboardButton(text="Меню", callback_data="menu"))
    return ikb


def admin_change_dates():
    ikb = InlineKeyboardMarkup()
    ikb.add(
        InlineKeyboardButton(text="Добавить запись", callback_data="add_date")).add(
        InlineKeyboardButton(text="Удалить запись", callback_data="change_date")).add(
        InlineKeyboardButton(text="Меню", callback_data="menu"))
    return ikb


def ikb_data(action, data):
    ikb = InlineKeyboardMarkup()
    for elem in data:
        ikb.add(InlineKeyboardButton(text=f"{elem}", callback_data=f"{action}{elem}"))
    return ikb


def cancel():
    rkb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    rkb.add(KeyboardButton(text="/cancel"))
    return rkb


def rkb_menu():
    rkb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    rkb.add(KeyboardButton(text="/menu"))
    return rkb


def ikb_confirm_action(action, data):
    ikb = InlineKeyboardMarkup()
    ikb.add(
        InlineKeyboardButton(text="Да", callback_data=callback_date.new(action=action, data=data)),
        InlineKeyboardButton(text="Нет", callback_data="menu"))
    return ikb



