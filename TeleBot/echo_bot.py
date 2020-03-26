import telebot
import time
import os
from telebot import types
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        'Greetings! I can show you PrivatBank exchange rates.\n' +
        'To get the exchange rates press /exchange.\n' +
        'To get help press /help.'
        )


@bot.message_handler(commands=['help'])
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            'Message Me', url='baidu.com'
        )
    )
    bot.send_message(
        message.chat.id,
        "lllllllllovemmmmmmmme",
        reply_markup=keyboard
    )

@bot.message_handler(commands=['exchange'])
def exchange_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('USD', callback_data='get-USD')
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton('EUR', callback_data='get-EUR'),
        telebot.types.InlineKeyboardButton('RUR', callback_data='get-RUR')
    )

    bot.send_message(message.chat.id, 'Click to choose:', reply_markup=keyboard)


if __name__ == '__main__':
    bot.polling(none_stop=True)