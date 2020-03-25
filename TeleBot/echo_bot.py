import telebot
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['/start'])
def bot_start(message):
    if message.text == '/start':
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, "欢迎使用机器人啊！\n试一下/help")

@bot.message_handler(commands=['help'])
def bot_help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, "你想要啥帮助？？")

if __name__ == '__main__':
    bot.polling()