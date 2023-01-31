import argparse
import os
import sys

import telegram
from dotenv import load_dotenv


def publish_photo_to_telegram(image, bot):
    chat_id = os.getenv('TELEGRAM_BOT_CHANEL', default='@alexnv_dvmn_bot_test')
    with open('./images/nasa_epic_epic_1b_20221115003634.png', 'rb') as image_file:
        bot.send_document(chat_id=chat_id, document=image_file)


def init_telegram_bot():
    telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

    if telegram_bot_token:
        return telegram.Bot(token=telegram_bot_token)


def init_args():
    parser = argparse.ArgumentParser(description='Программа загружает фото в какнал телеграмм')
    parser.add_argument('photo', help='Путь к фотографии, если не указан, будет загружено случайное фото', nargs='?')

    return parser.parse_args(sys.argv[1:])


if __name__ == "__main__":
    load_dotenv()
    args = init_args()
