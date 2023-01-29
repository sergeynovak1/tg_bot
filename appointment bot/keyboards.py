from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def admin_menu():
    ikb = InlineKeyboardMarkup()
    ikb.add(
        InlineKeyboardButton(text="Настроить расписание", callback_data=" ")).add(
        InlineKeyboardButton(text="Посмотреть записи", callback_data="appointments")).add(
        InlineKeyboardButton(text="Сделать рассылку", callback_data=" "))
    return ikb


def client_menu():
    ikb = ReplyKeyboardMarkup(resize_keyboard=True)
    ikb.add(
        KeyboardButton(text="Записаться на стрижку"))
    return ikb




