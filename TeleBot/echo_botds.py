import telebot
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "大噶猴啊！")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)
    
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(reply_to_message_id=message.message_id, chat_id=message.chat.id, text='可以帮你不？')
    
if __name__ == '__main__':
    bot.polling()
