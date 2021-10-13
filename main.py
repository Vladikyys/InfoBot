import re

import telebot
import configure
from telebot import types

bot = telebot.TeleBot(configure.config['token'])

name = ''
age = 0
gender = ''


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привіт', reply_markup=types.ReplyKeyboardRemove())
    msg = bot.send_message(message.chat.id, "Ваше ім'я?")
    bot.register_next_step_handler(msg, get_name)


def message_handler(message):
    if message.text == 'Інформація':
        bot.send_message(message.chat.id, f'Імя: {name}\nВік: {age}\nСтать: {gender}')
        bot.register_message_handler(message_handler)
    elif message.text == 'Налаштування':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        item1 = types.KeyboardButton(text='Змінити імя')
        item2 = types.KeyboardButton(text='Змінити вік')
        item3 = types.KeyboardButton(text='Змінити стать')
        item4 = types.KeyboardButton(text='Назад')

        markup.add(item1, item2, item3, item4)
        msg = bot.send_message(message.chat.id, 'Бажаєте щось змінити?', reply_markup=markup)
        bot.register_next_step_handler(msg, change)
    else:
        bot.reply_to(message, 'Ой, напевно, щось пішло не так')
        bot.register_message_handler(message_handler)


def change(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton(text='Назад')
    markup.add(item)
    if message.text == 'Змінити імя':
        msg = bot.send_message(message.chat.id, "Введіть ім'я:", reply_markup=markup)
        bot.register_next_step_handler(msg, change_name)
    elif message.text == 'Змінити вік':
        msg = bot.send_message(message.chat.id, 'Введіть вік:', reply_markup=markup)
        bot.register_next_step_handler(msg, change_age)
    elif message.text == 'Змінити стать':
        item1 = types.KeyboardButton(text='Жінка')
        item2 = types.KeyboardButton(text='Чоловік')
        markup.add(item1, item2)
        msg = bot.send_message(message.chat.id, 'Виберіть стать:', reply_markup=markup)
        bot.register_next_step_handler(msg, change_gender)
    elif message.text == 'Назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton(text='Інформація')
        item2 = types.KeyboardButton(text='Налаштування')
        markup.add(item1, item2)
        msg = bot.send_message(message.chat.id, 'Головне меню:', reply_markup=markup)
        bot.register_next_step_handler(msg, message_handler)
    else:
        bot.reply_to(message, 'Ой, напевно, щось пішло не так')


def change_name(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton(text='Змінити імя')
    item2 = types.KeyboardButton(text='Змінити вік')
    item3 = types.KeyboardButton(text='Змінити стать')
    item4 = types.KeyboardButton(text='Назад')

    markup.add(item1, item2, item3, item4)
    if message.text == 'Назад':
        msg = bot.send_message(message.chat.id, 'Бажаєте щось змінити?', reply_markup=markup)
        bot.register_next_step_handler(msg, change)
        return
    msg = try_set_name(message)
    if msg is None:
        msg = bot.send_message(message.chat.id, "Ім'я змінено", reply_markup=markup)
        bot.register_next_step_handler(msg, change)
    else:
        bot.register_next_step_handler(msg, change_name)


def change_age(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton(text='Змінити імя')
    item2 = types.KeyboardButton(text='Змінити вік')
    item3 = types.KeyboardButton(text='Змінити стать')
    item4 = types.KeyboardButton(text='Назад')
    markup.add(item1, item2, item3, item4)
    if message.text == 'Назад':
        msg = bot.send_message(message.chat.id, 'Бажаєте щось змінити?', reply_markup=markup)
        bot.register_next_step_handler(msg, change)
        return
    msg = try_set_age(message)
    if msg is None:
        msg = bot.send_message(message.chat.id, 'Вік змінено', reply_markup=markup)
        bot.register_next_step_handler(msg, change)
    else:
        bot.register_next_step_handler(msg, change_age)


def change_gender(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton(text='Змінити імя')
    item2 = types.KeyboardButton(text='Змінити вік')
    item3 = types.KeyboardButton(text='Змінити стать')
    item4 = types.KeyboardButton(text='Назад')
    markup.add(item1, item2, item3, item4)
    if message.text == 'Назад':
        msg = bot.send_message(message.chat.id, 'Бажаєте щось змінити?', reply_markup=markup)
        bot.register_next_step_handler(msg, change)
        return
    msg = try_set_gender(message)
    if msg is None:
        msg = bot.send_message(message.chat.id, 'Стать змінена', reply_markup=markup)
        bot.register_next_step_handler(msg, change)
    else:
        bot.register_next_step_handler(msg, change_gender)


def get_name(message):
    msg = try_set_name(message)
    if msg is None:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        item = types.KeyboardButton(text='Назад')
        markup.add(item)
        msg = bot.send_message(message.chat.id, 'Скільки років?', reply_markup=markup)
        bot.register_next_step_handler(msg, get_age)
    else:
        bot.register_next_step_handler(msg, get_name)


def try_set_name(message):
    global name
    if re.match(r'([А-Я]?[а-я]+)$', message.text) or re.match('([A-Z]?[a-z]+)$', message.text):
        if 2 < len(message.text) < 20:
            name = message.text
            return None
        else:
            return bot.reply_to(message, 'Введіть імя в діапазоні від 2 до 20')

    else:
        return bot.reply_to(message, 'Введіть букви, будь ласка!')


def get_age(message):
    if message.text == 'Назад':
        msg = bot.send_message(message.chat.id, "Ваше ім'я?", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, get_name)
        return
    msg = try_set_age(message)
    if msg is None:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton(text='Жінка')
        item2 = types.KeyboardButton(text='Чоловік')
        item3 = types.KeyboardButton(text='Назад')
        markup.add(item1, item2, item3)

        msg = bot.send_message(message.chat.id, 'Ваша стать?', reply_markup=markup)
        bot.register_next_step_handler(msg, get_gender)
    else:
        bot.register_next_step_handler(msg, get_age)


def try_set_age(message):
    global age
    if re.match(r'([1-9]|[0-9]{2})$', message.text):
        age = int(message.text)
        return None
    else:
        return bot.reply_to(message, 'Введіть цифри, будь ласка!')


def get_gender(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(text='Інформація')
    item2 = types.KeyboardButton(text='Налаштування')
    markup.add(item1, item2)
    if message.text == 'Назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton(text='Назад')
        markup.add(item1)
        msg = bot.send_message(message.chat.id, 'Скільки років?', reply_markup=markup)
        bot.register_next_step_handler(msg, get_age)
        return
    msg = try_set_gender(message)
    if msg is None:
        msg = bot.send_message(message.chat.id, 'Головне меню:', reply_markup=markup)
        bot.register_next_step_handler(msg, message_handler)
    else:
        bot.register_next_step_handler(msg, get_gender)


def try_set_gender(message):
    global gender
    if message.text == 'Жінка':
        gender = message.text
        return None
    elif message.text == 'Чоловік':
        gender = message.text
        return None
    else:
        return bot.send_message(message.chat.id, 'Виберіть варінт по кнопці')


if __name__ == '__main__':
    bot.polling(none_stop=True)

