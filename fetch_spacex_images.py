import argparse
import logging
import sys
from pathlib import Path
import requests
from common_functions import save_image_to_file_from_url

def get_lastest_spacex_lauch_images(flight_id):

    if flight_id:
        url = 'https://api.spacexdata.com/v5/launches'
        payload = {
            'flight_id': flight_id
        }
    else:
        url = 'https://api.spacexdata.com/v5/launches/latest'
        payload = {

        }
    response = requests.get(url, params=payload)
    response.raise_for_status()

    launch_json = response.json()
    if flight_id:
        # у запусков может не быть изображений, вернем только те запуски, где больше 5 картинок
        for launch_info in launch_json:
            if len(launch_info['links']['flickr']['original']) >= 5:
                launch_image_urls = launch_info['links']['flickr']['original']
                break
    else:
        launch_image_urls = launch_json['links']['flickr']['original']
    return launch_image_urls


def fetch_spacex_last_launch(flight_id):
    Path("./images").mkdir(parents=True, exist_ok=True)

    launch_images = get_lastest_spacex_lauch_images(flight_id)
    for index, image_url in enumerate(launch_images):
        logging.info(f"Downloading image from url: {image_url} to ./images/spacex_{index}.jpeg")
        save_image_to_file_from_url(image_url, f"./images/spacex_{index}.jpeg")


def init_args():
    parser = argparse.ArgumentParser(description='Программа загружает фото запусков SpaceX по указанному ID запуска')
    parser.add_argument('id', help='ID Запуска', nargs='?')

    return parser.parse_args(sys.argv[1:])


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    args = init_args()
    fetch_spacex_last_launch(args.id)