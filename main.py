import os

import telegram
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()
    chat_id = '@alexnv_dvmn_bot_test'
    telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if telegram_bot_token:
        bot = telegram.Bot(token=telegram_bot_token)
        bot.send_message(chat_id=chat_id, text="I'm sorry Dave I'm afraid I can't do that.")