import argparse
import os
import random
import sys
import time
from os.path import join

import telegram
from dotenv import load_dotenv

from common_functions import get_imagefolder


def publish_photo_to_telegram(image, bot):
    chat_id = os.getenv('TELEGRAM_BOT_CHANEL')
    with open(image, 'rb') as image_file:
        bot.send_document(chat_id=chat_id, document=image_file)


def publish_files_to_telegram(root, files, timeout, bot):
    for file in files:
        publish_photo_to_telegram(join(root, file), bot)
        time.sleep(timeout)


def publish_photos_to_telegram(timeout, bot):
    for root, dirs, files in list(os.walk(get_imagefolder())):
        publish_files_to_telegram(root, files, timeout, bot)

    while True:
        for root, dirs, files in list(os.walk(get_imagefolder())):
            random.shuffle(files)
            publish_files_to_telegram(root, files, timeout, bot)


def init_telegram_bot():
    telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if telegram_bot_token:
        return telegram.Bot(token=telegram_bot_token)


def init_args():
    parser = argparse.ArgumentParser(description='Программа загружает фото из каталога в какнал телеграмм')
    parser.add_argument('timeout', help='Задержка публикации в часах', nargs='?', default="4")

    return parser.parse_args(sys.argv[1:])


if __name__ == "__main__":
    load_dotenv()
    args = init_args()
    tgbot = init_telegram_bot()
    if tgbot:
        timeout_in_seconds = int(args.timeout) * 60 * 60
        publish_photos_to_telegram(timeout_in_seconds, tgbot)
