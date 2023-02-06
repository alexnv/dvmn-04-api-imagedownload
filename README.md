# Отправка изображений в телеграм через бота

Скрипты скачивают фото из различных источников

* fetch_nasa_apod_images.py - скачивает из каталога NASA Astronomy Picture of the Day
* fetch_nasa_epic_images.py - скачивает из каталога DSCOVR's Earth Polychromatic Imaging Camera
* fetch_spacex_images.py - скачивает из каталога Space X Launch images

Для вызова программы необходимо запустить скрипт с первым параметром в виде задержки в часах для публикации фото.
Например:

```
python publish_photos_to_telegram.py 4
```

```
usage: publish_photos_to_telegram.py [-h] [timeout]

Программа загружает фото из каталога в канал телеграмм

positional arguments:
  timeout     Задержка публикации в часах

optional arguments:
  -h, --help  show this help message and exit

```

### Как установить

Для получения API ключа NASA Astronomy Picture of the Day, необходимо

1. Зарегистрироваться на сервисе [https://api.nasa.gov/#apod](https://api.nasa.gov/#apod)

После этого появится ваш API ключ вида `0PrJuaZsdq3Lv7B81YcFtyYt4Uk1jKb8YDUn0oax`
Данный ключ необходимо добавить в файл `.env` в каталоге с программой указав значение для переменной `APOD_KEY=`

Для отправки сообщений в телеграмм необходимо получить API ключ бота и записать его добавить в файл `.env` в каталоге с
программой указав значение для переменной `TELEGRAM_BOT_TOKEN=`, в параметр `TELEGRAM_BOT_CHANEL=` ввести имя канала для
отправки изображений

Python3 должен быть уже установлен.
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:

```
pip install -r requirements.txt
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).