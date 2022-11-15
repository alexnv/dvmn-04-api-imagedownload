import datetime
import os
from pathlib import Path
from urllib.parse import urlsplit, unquote

import requests
from dotenv import load_dotenv


def save_image_to_file_from_url(image_url, file_name):
    response = requests.get(image_url)
    response.raise_for_status()

    with open(file_name, 'wb') as file:
        file.write(response.content)


def get_lastest_spacex_lauch_images():
    url = 'https://api.spacexdata.com/v5/launches'
    payload = {
        'flight_id': '5eb87d47ffd86e000604b38a'
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()

    launch_json = response.json()
    launch_image_urls = launch_json[98]['links']['flickr']['original']
    return launch_image_urls


def fetch_spacex_last_launch():
    Path("./images").mkdir(parents=True, exist_ok=True)

    launch_images = get_lastest_spacex_lauch_images()
    for index, image_url in enumerate(launch_images):
        save_image_to_file_from_url(image_url, f"./images/spacex{index}.jpeg")


def get_file_extension_from_url(url):
    url_structure = urlsplit(url)
    path = unquote(url_structure.path)

    (head, tail) = os.path.split(path)
    (root, ext) = os.path.splitext(tail)

    return ext


def fetch_nasa_apod():
    url = 'https://api.nasa.gov/planetary/apod'
    payload = {
        'api_key': os.getenv("APOD_KEY"),
        'count': '5'
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()

    image_urls = response.json()
    Path("./images").mkdir(parents=True, exist_ok=True)
    for index, image_data in enumerate(image_urls):
        image_extension = get_file_extension_from_url(image_data['url'])
        print(f"Downloading image from url: {image_data['url']}")
        if image_extension:
            save_image_to_file_from_url(image_data['url'], f"./images/nasa_apod_{index}{image_extension}")


def fetch_nasa_epic():
    url = 'https://api.nasa.gov/EPIC/api/natural/images'
    payload = {
        'api_key': os.getenv("APOD_KEY")
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()

    images = response.json()
    for image in images:
        image_name = image['image']
        image_date = datetime.datetime.fromisoformat(image['date']).strftime("%Y/%m/%d")

        url = f'https://api.nasa.gov/EPIC/archive/natural/{image_date}/png/{image_name}.png'
        response = requests.get(url, params=payload)
        response.raise_for_status()

        with open(f'./images/nasa_epic_{image_name}.png', 'wb') as file:
            file.write(response.content)


if __name__ == '__main__':
    load_dotenv()
    APOD_KEY = os.getenv("APOD_KEY")
    if APOD_KEY:
        # fetch_nasa_apod()
        fetch_nasa_epic()
