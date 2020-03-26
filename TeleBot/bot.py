import telegram
from config import TOKEN

bot = telegram.Bot(TOKEN)

def main():
    updates = bot.getUpdates()
    for update in updates:
        text = update['message']['text']
        message_id = update['message_id']
        print(message_id, text)

if __name__ == '__main__':
    main()