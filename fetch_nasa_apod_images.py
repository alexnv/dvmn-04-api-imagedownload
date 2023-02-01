import logging
import os

import requests
from dotenv import load_dotenv

from common_functions import save_image_to_file_from_url, get_file_extension_from_url, get_imagefolder_filename, \
    get_imagefolder


def fetch_nasa_apod(apod_key):
    url = 'https://api.nasa.gov/planetary/apod'
    payload = {
        'api_key': apod_key,
        'count': '5'
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()

    image_urls = response.json()
    get_imagefolder().mkdir(parents=True, exist_ok=True)
    for index, image_data in enumerate(image_urls):
        if image_data['media_type'] == 'image':
            image_extension = get_file_extension_from_url(image_data['url'])
            file_name = get_imagefolder_filename(f'nasa_apod_{index}{image_extension}')
            logging.info(f"Downloading image from url: {image_data['url']} to {file_name}")
            if image_extension:
                save_image_to_file_from_url(image_data['url'], file_name)


def main():
    logging.getLogger().setLevel(logging.INFO)
    load_dotenv()
    APOD_KEY = os.environ["APOD_KEY"]
    if APOD_KEY:
        fetch_nasa_apod(APOD_KEY)
    else:
        logging.error("Не задано значение переменной окружения APOD_KEY")


if __name__ == '__main__':
    main()
