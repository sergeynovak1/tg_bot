import telebot
import config
import re

from telebot import types
from main import *

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    sti = open('hello.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    Z(message, "Привет, {0.first_name}! \nЧто хочешь подсчитать".format(message.from_user), "Количество сочетаний", "Количество перестановок", "Количество размещений")


@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "Количество сочетаний"):
        Z(message, "Поподробнее", "Количество сочетаний с повторениями", "Количество сочетаний без повторений", "Вернуться в главное меню")
    elif (message.text == "Количество перестановок"):
        Z(message, "Поподробнее", "Количество перестановок с повторениями", "Количество перестановок без повторений", "Вернуться в главное меню")
    elif (message.text == "Количество размещений"):
        Z(message, "Поподробнее", "Количество размещений с повторениями", "Количество размещений без повторений", "Вернуться в главное меню")
    elif (message.text == "Вернуться в главное меню"):
        Z(message, "Вы вернулись в главное меню", "Количество сочетаний", "Количество перестановок", "Количество размещений")
    elif (message.text == "Количество сочетаний с повторениями"):
        P(message, CS)
    elif (message.text == "Количество сочетаний без повторений"):
        P(message, CB)
    elif (message.text == "Количество перестановок с повторениями"):
        PR(message, PS)
    elif (message.text == "Количество перестановок без повторений"):
        PR(message, PB)
    elif (message.text == "Количество размещений с повторениями"):
        P(message, AS)
    elif (message.text == "Количество размещений без повторений"):
        P(message, AB)
    else:
        sti = open('notfound.webp', 'rb')
        bot.send_sticker(message.chat.id, sti)
        bot.send_message(message.chat.id, text="На такую команду я не запрограммирован..")


def Z(message, txt, *btns):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for btn in btns:
        markup.row(btn)
    bot.send_message(message.chat.id, text=txt, reply_markup=markup)


def P(message, f):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton("Вернуться в главное меню")
    markup.add(back)
    bot.send_message(message.from_user.id, 'Введите числа n и k через пробел.', reply_markup=markup)
    bot.register_next_step_handler(message, f)


def PR(message, f):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton("Вернуться в главное меню")
    markup.add(back)
    bot.send_message(message.from_user.id, 'Введите числа через пробел.', reply_markup=markup)
    bot.register_next_step_handler(message, f)


def F(message, txt, f):
    try:
        n, k = re.split(' ', message.text, maxsplit=1)
        n = int(n)
        k = int(k)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(back)
        bot.send_message(message.from_user.id, 'Результат: ' + str(f(n, k)), reply_markup=markup)
        sti = open('ok.webp', 'rb')
        bot.send_sticker(message.chat.id, sti)
    except Exception:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Вернуться в главное меню")
        btn1 = types.KeyboardButton(txt)
        markup.add(btn1, back)
        if (message.text == "Вернуться в главное меню"):
            Z(message, "Вы вернулись в главное меню", "Количество сочетаний", "Количество перестановок", "Количество размещений")
        else:
            sti = open('error.webp', 'rb')
            bot.send_sticker(message.chat.id, sti)
            bot.send_message(message.from_user.id, 'Вы ввели данные не в правильном формате.', reply_markup=markup, parse_mode='Markdown')



def FR(message, txt, f):
    try:
        n = re.split(' ', message.text)
        n = [int(m) for m in n]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(back)
        bot.send_message(message.from_user.id, 'Результат: ' + str(f(n)), reply_markup=markup)
        sti = open('ok.webp', 'rb')
        bot.send_sticker(message.chat.id, sti)
    except Exception:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Вернуться в главное меню")
        btn1 = types.KeyboardButton(txt)
        markup.add(btn1, back)
        if (message.text == "Вернуться в главное меню"):
            Z(message, "Вы вернулись в главное меню", "Количество сочетаний", "Количество перестановок", "Количество размещений")
        else:
            sti = open('error.webp', 'rb')
            bot.send_sticker(message.chat.id, sti)
            bot.send_message(message.from_user.id, 'Вы ввели данные не в правильном формате.', reply_markup=markup, parse_mode='Markdown')


def CS(message):
    F(message, "Количество сочетаний с повторениями", Cs)


def CB(message):
    F(message, "Количество сочетаний без повторений", Cb)


def AS(message):
    F(message, "Количество размещений с повторениями", As)


def AB(message):
    F(message, "Количество размещений без повторений", Ab)


def PS(message):
    FR(message, "Количество перестановок с повторениями", Ps)


def PB(message):
    FR(message, "Количество перестановок без повторений", Pb)


bot.polling(none_stop=True)