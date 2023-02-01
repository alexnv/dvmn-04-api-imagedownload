import argparse
import logging
import sys

import requests

from common_functions import save_image_to_file_from_url, get_imagefolder_filename, get_imagefolder


def get_lastest_spacex_lauch_images(flight_id="latest"):
    url = f'https://api.spacexdata.com/v5/launches/{flight_id}'
    response = requests.get(url)
    response.raise_for_status()

    launch_info = response.json()
    # у запусков может не быть изображений, вернем только те запуски, где больше 5 картинок
    launch_image_urls = launch_info['links']['flickr']['original']
    if len(launch_image_urls) >= 5:
        return launch_image_urls
    return []


def fetch_spacex_last_launch(flight_id):
    if flight_id != "latest" and len(flight_id) != 24:
        raise ValueError("Длинна ID запуска должна быть 24 символа, либо пустая строка")

    get_imagefolder().mkdir(parents=True, exist_ok=True)

    launch_images = get_lastest_spacex_lauch_images(flight_id)
    for index, image_url in enumerate(launch_images):
        file_name = get_imagefolder_filename(f"spacex_{index}.jpeg")
        logging.info(f"Downloading image from url: {image_url} to {file_name}")
        save_image_to_file_from_url(image_url, file_name)


def init_args():
    parser = argparse.ArgumentParser(description='Программа загружает фото запусков SpaceX по указанному ID запуска')
    parser.add_argument('id', help='ID Запуска', nargs='?', default="latest")

    return parser.parse_args(sys.argv[1:])


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    args = init_args()
    fetch_spacex_last_launch(args.id)
