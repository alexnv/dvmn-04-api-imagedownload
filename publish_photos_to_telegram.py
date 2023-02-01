import argparse
import logging
import os
import random
import sys
import time
from os.path import join

import requests
import telegram
from dotenv import load_dotenv

from common_functions import get_imagefolder


def publish_photo_to_telegram(image, bot, chat_id):
    with open(image, 'rb') as image_file:
        bot.send_document(chat_id=chat_id, document=image_file)


def publish_files_to_telegram(root, files, timeout, bot, chat_id):
    for file in files:
        logging.info(f"send photo {join(root, file)} to telegram")
        publish_photo_to_telegram(join(root, file), bot, chat_id)
        time.sleep(timeout)


def publish_photos_to_telegram(timeout, bot, chat_id):
    first_run = True
    error_delay = 1
    while True:
        try:
            for root, dirs, files in os.walk(get_imagefolder()):
                if not first_run:
                    random.shuffle(files)
                publish_files_to_telegram(root, files, timeout, bot, chat_id)
                first_run = False
        except (telegram.error.NetworkError, requests.Timeout, requests.ConnectionError) as error:
            time.sleep(error_delay)
            error_delay = 30
            logging.error(error)


def init_telegram_bot(telegram_bot_token):
    if telegram_bot_token:
        return telegram.Bot(token=telegram_bot_token)


def init_args():
    parser = argparse.ArgumentParser(description='Программа загружает фото из каталога в какнал телеграмм')
    parser.add_argument('timeout', help='Задержка публикации в часах', nargs='?', default="4")

    return parser.parse_args(sys.argv[1:])


if __name__ == "__main__":
    load_dotenv()
    args = init_args()

    chat_id = os.environ['TELEGRAM_BOT_CHANEL']
    telegram_bot_token = os.environ['TELEGRAM_BOT_TOKEN']

    tgbot = init_telegram_bot(telegram_bot_token)
    logging.getLogger().setLevel(logging.INFO)
    if tgbot:
        timeout_in_seconds = int(args.timeout) * 60 * 60
        publish_photos_to_telegram(timeout_in_seconds, tgbot, chat_id)
