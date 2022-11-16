import logging
import os
from datetime import datetime

import requests
from dotenv import load_dotenv


def fetch_nasa_epic(apod_key):
    url = 'https://api.nasa.gov/EPIC/api/natural/images'
    payload = {
        'api_key': apod_key
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()

    images = response.json()
    for image in images:
        image_name = image['image']
        image_date = datetime.fromisoformat(image['date']).strftime("%Y/%m/%d")

        url = f'https://api.nasa.gov/EPIC/archive/natural/{image_date}/png/{image_name}.png'

        logging.info(f"Downloading image from url: {url} to ./images/nasa_epic_{image_name}.png")

        response = requests.get(url, params=payload)
        response.raise_for_status()

        with open(f'./images/nasa_epic_{image_name}.png', 'wb') as file:
            file.write(response.content)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    load_dotenv()
    APOD_KEY = os.getenv("APOD_KEY")
    if APOD_KEY:
        fetch_nasa_epic(APOD_KEY)