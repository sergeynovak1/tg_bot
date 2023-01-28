from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

admin_menu = InlineKeyboardMarkup()
admin_menu.add(
    InlineKeyboardButton(text="Настроить расписание", callback_data=" ")).add(
    InlineKeyboardButton(text="Посмотреть записи", callback_data="appointments")).add(
    InlineKeyboardButton(text="Сделать рассылку", callback_data=" "))

admin_change_appointments = InlineKeyboardMarkup()
admin_change_appointments.add(
    InlineKeyboardButton(text="Добавить запись", callback_data=" ")).add(
    InlineKeyboardButton(text="Удалить запись", callback_data=" ")
)

menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(
    KeyboardButton(text="Меню")
)


