import logging
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import MessageHandler

from config import TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def message_handler(update:Update, context:CallbackContext):
    update.message.reply_text(
        text = 'Hellooooo',
    )

def main():
    updater = Updater(token=TOKEN, use_context=True)
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.all, callback=message_handler()))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()