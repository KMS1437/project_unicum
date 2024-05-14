#Экономика
# -*- coding: utf-8 -*-

from telebot import types
import telebot
import json
import os
from tkinter import Tk, Label

bot = telebot.TeleBot("TOKEN")

def get_balance(user_id):
    if user_id in balances:
        income = balances[user_id].get('income', 0)
        expenses = balances[user_id].get('expenses', 0)
        return income - expenses
    else:
        return 0

def update_balances():
    with open("balances.json", "w") as file:
        json.dump(balances, file)

@bot.message_handler(commands=['plus'])
def add_income(message):
    try:
        bot.send_message(message.chat.id, "💲 *Введите доход:*", parse_mode="Markdown")
        bot.register_next_step_handler(message, process_income_step)
        income_tk(message)
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ *Error:* {e}", parse_mode="Markdown")

def process_income_step(message):
    user_id = message.from_user.id
    if user_id not in balances:
        balances[user_id] = {"income": 0, "expenses": 0}
    try:
        income = float(message.text)
        balances[user_id]["income"] += income
        update_balances()
        bot.send_message(message.chat.id,
                         f"✅ *Доход в размере {income} добавлен.\nТекущий баланс:* {get_balance(user_id)}", parse_mode="Markdown")
    except ValueError:
        bot.send_message(message.chat.id, f"❌ *Некорректное значение. Пожалуйста, введите число.*", parse_mode="Markdown")

@bot.message_handler(commands=['minus'])
def add_expenses(message):
    try:
        bot.send_message(message.chat.id, "💸 *Введите расход:*", parse_mode="Markdown")
        bot.register_next_step_handler(message, process_expenses_step)
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ *Error: {e}*", parse_mode="Markdown")

def process_expenses_step(message):
    user_id = message.from_user.id
    if user_id not in balances:
        balances[user_id] = {"income": 0, "expenses": 0}
    try:
        expenses = float(message.text)
        balances[user_id]["expenses"] += expenses
        update_balances()
        bot.send_message(message.chat.id,
                         f"✅ *Расход в размере {expenses} добавлен.\nТекущий баланс:* {get_balance(user_id)}", parse_mode="Markdown")
    except ValueError:
        bot.send_message(message.chat.id, f"❌ *Некорректное значение. Пожалуйста, введите число.*", parse_mode="Markdown")

@bot.message_handler(commands=['balance'])
def get_balance_command(message):
    user_id = message.from_user.id
    if user_id in balances:
        income = balances[user_id].get('income', 0)
        expenses = balances[user_id].get('expenses', 0)
        balance = income - expenses
        bot.send_message(message.chat.id, f"<b>💰 Доход за месяц:</b> {income} руб.\n💸 <b>Расход за месяц:</b> {expenses} руб.\n🔵 <b>Баланс:</b> {balance} руб.", parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, "*У вас нет записей о доходах и расходах. Напишите /plus или /minus*", parse_mode="Markdown")

if os.path.exists("balances.json"):
    with open("balances.json", "r") as file:
        balances = json.load(file)
        user_id = None
        if user_id not in balances:
            balances[user_id] = {"income": 0, "expenses": 0}
else:
    balances = {}

if os.path.exists('persons.json'):
    with open('persons.json', 'r') as file:
        persons = json.load(file)
        admins = persons['admins']
        bans = persons['bans']
else:
    print("Файл persons.json отсутствует. Пожалуйста, убедитесь, что он создан и заполнен корректно.")


@bot.message_handler(commands=['code'])
def send_code(message):
    user_id = message.from_user.id
    print(f"ID пользователя {message.from_user.first_name}:", user_id)
    if user_id in admins:
        with open('economic.py', 'r', encoding='utf-8') as file:
            bot.send_message(message.chat.id, "*Код бота:*", parse_mode="Markdown")
            bot.send_document(message.chat.id, file)

    else:
        bot.send_message(message.chat.id, "Вы не админ. У вас нет доступа к этой команде")



@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "*👋 Привет! Я бот по балансу ваших денег и работаю на Дмитрия Борисовича. Чем могу помочь?*",
                     parse_mode="Markdown")
    bot.send_message(message.chat.id, "Нажмите на кнопку или введите задачу:",
                     reply_markup=get_keyboard())


@bot.message_handler(commands=['info'])
def handle_info(message):
    bot.send_message(message.chat.id,
                     f'*Создатель:* @misakamozin\n*Дата первого создания:* 27 марта 2024\n*Описание проекта: * Проект был создан при поддержке учебного заведения "ЦДНИТТ при КузГТУ «УникУм»". Этот проект может помочь следить за тратами и балансом.\n*Используемые библиотеки: * telebot, re, json, os',
                     parse_mode="Markdown")


@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_input = message.text
    if message.from_user.id in bans:
        bot.send_message(message.chat.id, f"⚡ Вам заблокирован доступ к боту, {message.from_user.first_name}.")
    elif user_input == "💻 Как пользоваться этим ботом?":
        bot.send_message(message.chat.id,
                         f"⚜ <b>{message.from_user.first_name}, бот поддерживает эти команды:\n/minus</b> - после ввода команды вы вводите свой расход\n<b>/plus</b> - после ввода этой команды вы вводите свой заработок\n<b>/balance</b> - вы увидите свой баланс", parse_mode="HTML")
    elif user_input == "❓ Обновления проекта":
        markup = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton("Канал по проекту", url='https://t.me/project_unicum')
        markup.add(button1)
        bot.send_message(message.chat.id, "Обновления проекта:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Эта команд не поддерживается")


def get_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2)
    button1 = types.KeyboardButton("💻 Как пользоваться этим ботом?")
    button2 = types.KeyboardButton("❓ Обновления проекта")
    markup.add(button1, button2)
    return markup

if __name__ == "__main__":
    bot.polling(none_stop=True)
