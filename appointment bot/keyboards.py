from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def admin_menu():
    ikb = InlineKeyboardMarkup()
    ikb.add(
        InlineKeyboardButton(text="Настроить расписание", callback_data="change_appointments")).add(
        InlineKeyboardButton(text="Посмотреть записи", callback_data="appointments")).add(
        InlineKeyboardButton(text="Сделать рассылку", callback_data=" "))
    return ikb


def client_menu():
    ikb = ReplyKeyboardMarkup(resize_keyboard=True)
    ikb.add(
        KeyboardButton(text="Записаться на стрижку"))
    return ikb


def admin_change_dates():
    ikb = InlineKeyboardMarkup()
    ikb.add(
        InlineKeyboardButton(text="Добавить запись", callback_data="add_date")).add(
        InlineKeyboardButton(text="Удалить запись", callback_data="change_date")).add(
        InlineKeyboardButton(text="Меню", callback_data="menu"))
    return ikb


def ikb_dates(dates):
    ikb = InlineKeyboardMarkup()
    for date in dates:
        ikb.add(InlineKeyboardButton(text=f"{date}", callback_data=f"date{date}"))
    return ikb


def cancel():
    rkb = ReplyKeyboardMarkup(resize_keyboard=True)
    rkb.add(KeyboardButton(text="/cancel"))
    return rkb


menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(
    KeyboardButton(text="Меню")
)




