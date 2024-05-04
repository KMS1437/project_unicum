#Экономика
# -*- coding: utf-8 -*-

from telebot import types
import random
import telebot
import re
import json
import os

bot = telebot.TeleBot("TOKEN")

total_income = 0
total_expenses = 0
balances = {}

if os.path.exists("balances.json"):
    with open("balances.json", "r") as file:
        balances = json.load(file)
        income = balances['income']
        expenses = balances['expenses']

@bot.message_handler(commands=['plus'])
def add_income(message):
    try:
        bot.send_message(message.chat.id, "💲 Введите доход:")
        bot.register_next_step_handler(message, process_income_step)
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error: {e}")


def process_income_step(message):
    user_id = message.from_user.id
    global balances
    if user_id not in balances:
        balances[user_id] = {"income": 0, "expenses": 0}
    try:
        income = float(message.text)
        balances[user_id]["income"] += income
        update_balances()
        bot.send_message(message.chat.id,
                         f"✅ Доход в размере {income} добавлен. Текущий баланс: {get_balance(user_id)}")
    except ValueError:
        bot.send_message(message.chat.id, f"❌ Некорректное значение. Пожалуйста, введите число.")

@bot.message_handler(commands=['minus'])
def add_expenses(message):
    try:
        bot.send_message(message.chat.id, "💸 Введите расход:")
        bot.register_next_step_handler(message, process_expenses_step)
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error: {e}")


def process_expenses_step(message):
    user_id = message.from_user.id
    global balances
    if user_id not in balances:
        balances[user_id] = {"income": 0, "expenses": 0}
    try:
        expenses = float(message.text)
        balances[user_id]["expenses"] += expenses
        update_balances()
        bot.send_message(message.chat.id,
                         f"✅ Расход в размере {expenses} добавлен. Текущий баланс: {get_balance(user_id)}")
    except ValueError:
        bot.send_message(message.chat.id, f"❌ Некорректное значение. Пожалуйста, введите число.")

@bot.message_handler(commands=['balance'])
def get_balance(message):
    user_id = message.from_user.id
    balance = get_balance(user_id)
    bot.send_message(message.chat.id, f"💰 Доход за месяц: {balances[user_id]['income']} руб.\n💸 Расход за месяц: {balances[user_id]['expenses']} руб.\n🔵 Баланс: {balance} руб.")
    return balances[user_id]["income"] - balances[user_id]["expenses"]

def update_balances():
    with open("balances.json", "w") as file:
        json.dump(balances, file)

if os.path.exists('persons.json'):
    with open('persons.json', 'r') as file:
        persons = json.load(file)
        admins = persons['admins']
        bans = persons['bans']
else:
    print("Файл persons.json не существует. Пожалуйста, убедитесь, что он создан и заполнен корректно.")


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


def replace_superscript(text):
    superscripts = {
        '0': '⁰',
        '1': '¹',
        '2': '²',
        '3': '³',
        '4': '⁴',
        '5': '⁵',
        '6': '⁶',
        '7': '⁷',
        '8': '⁸',
        '9': '⁹'
    }

    def replace_match(match):
        return superscripts.get(match.group(0)[1], match.group(0))

    pattern = re.compile(r"\^(\d)")
    result = re.sub(pattern, replace_match, text)
    return result

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "*👋 Привет! Я бот по балансу ваших денег и работаю на Дмитрия Борисовича. Чем могу помочь?*",
                     parse_mode="Markdown")
    bot.send_message(message.chat.id, "Нажмите на кнопку или введите задачу:",
                     reply_markup=get_keyboard())


@bot.message_handler(commands=['info'])
def handle_info(message):
    bot.send_message(message.chat.id,
                     f'*Создатель:* @misakamozin\n*Дата первого создания:* 27 марта 2024\n*Описание проекта: * Проект был создан при поддержке учебного заведения "ЦДНИТТ при КузГТУ «УникУм»". Этот проект может помочь студентам сверить свой ответ по алгебре или физике с ответом бота.\n*Используемые библиотеки: * telebot, random, re, sympy, json, os',
                     parse_mode="Markdown")


@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_input = message.text
    if message.from_user.id in bans:
        bot.send_message(message.chat.id, f"⚡ Вам заблокирован доступ к боту, {message.from_user.first_name}.")
    elif user_input == "🏆 Миша испорченный до невозможности":
        bot.send_message(message.chat.id, f"⚜ Однозначно, {message.from_user.first_name}!")
    elif user_input == "💀 Насколько ты Паскарь?":
        chance = random.randrange(1, 100)
        bot.send_message(message.chat.id, f"⚜ {message.from_user.first_name}, вы Паскарь на {chance}%")
    elif user_input == "💻 Как пользоваться этим ботом?":
        bot.send_message(message.chat.id,
                         f"⚜ {message.from_user.first_name}, напишите команду /minus, /plus, /balance.")
    elif user_input == "❓ Обновления проекта":
        markup = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton("Канал по проекту", url='https://t.me/project_unicum')
        markup.add(button1)
        bot.send_message(message.chat.id, "Обновления проекта:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Эта команд не поддерживается")


def get_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2)
    button1 = types.KeyboardButton("🏆 Миша испорченный до невозможности")
    button2 = types.KeyboardButton("💻 Как пользоваться этим ботом?")
    button3 = types.KeyboardButton("💀 Насколько ты Паскарь?")
    button4 = types.KeyboardButton("❓ Обновления проекта")
    markup.add(button1, button2, button3, button4)
    return markup


if __name__ == "__main__":
    bot.polling(none_stop=True)
