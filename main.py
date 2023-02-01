import logging
import os

import telegram
from dotenv import load_dotenv

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    load_dotenv()
    chat_id = os.environ['TELEGRAM_BOT_CHANEL']
    telegram_bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    if telegram_bot_token:
        bot = telegram.Bot(token=telegram_bot_token)
        bot.send_message(chat_id=chat_id, text="I'm sorry Dave I'm afraid I can't do that.")
        bot.send_document(chat_id=chat_id, document=open('./images/nasa_epic_epic_1b_20221115003634.png', 'rb'))
    else:
        logging.error("Не задано значение переменной окружения TELEGRAM_BOT_TOKEN")
