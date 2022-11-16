import logging
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from common_functions import save_image_to_file_from_url, get_file_extension_from_url

def fetch_nasa_apod(apod_key):
    url = 'https://api.nasa.gov/planetary/apod'
    payload = {
        'api_key': apod_key,
        'count': '5'
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()

    image_urls = response.json()
    Path("./images").mkdir(parents=True, exist_ok=True)
    for index, image_data in enumerate(image_urls):
        image_extension = get_file_extension_from_url(image_data['url'])
        logging.info(f"Downloading image from url: {image_data['url']} to ./images/nasa_apod_{index}{image_extension}")
        if image_extension:
            save_image_to_file_from_url(image_data['url'], f"./images/nasa_apod_{index}{image_extension}")


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    load_dotenv()
    APOD_KEY = os.getenv("APOD_KEY")
    if APOD_KEY:
        fetch_nasa_apod(APOD_KEY)