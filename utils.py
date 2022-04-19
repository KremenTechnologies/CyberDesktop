import ctypes
import json
import struct

import httpx
from PIL import Image, ImageDraw, ImageFont

days = [
    'Понедельник',
    'Вторник',
    'Среда',
    'Четверг',
    'Пятница',
    'Суббота',
    'Воскресенье'
]


def is_64_windows():
    """Find out how many bits is OS. """
    return struct.calcsize('P') * 8 == 64


def get_sys_parameters_info():
    """Based on if this is 32bit or 64bit returns correct version of SystemParametersInfo function. """
    return ctypes.windll.user32.SystemParametersInfoW if is_64_windows() \
        else ctypes.windll.user32.SystemParametersInfoA


def change_wallpaper(path: str):
    sys_parameters_info = get_sys_parameters_info()
    r = sys_parameters_info(20, 0, path, 3)

    if not r:
        print(ctypes.WinError())


class Settings:
    def __init__(self):
        self.file = 'settings.json'
        self.__load_file()

    def __load_file(self):
        self.data = json.load(open(self.file, 'rb'))

    def get(self, key: str):
        return self.data.get(key)


class Exchange:
    def __init__(self, api_url: str):
        self.api_url = api_url
        self.exchange = {}

    def __fetch_data(self) -> None:
        self.exchange = httpx.get(self.api_url).json()

    def get(self) -> dict:
        try:
            self.__fetch_data()
        except Exception as e:
            print(e)
        _usd_exchange = 0.00
        _euro_exchange = 0.00

        for currency in self.exchange:
            if currency['r030'] == 840:
                _usd_exchange = currency['rate']
            if currency['r030'] == 978:
                _euro_exchange = currency['rate']

        return {'usd': _usd_exchange, 'euro': _euro_exchange}


class ImageBuilder:
    def __init__(self, width: int, height: int, bg: tuple):
        self.width = width
        self.height = height
        self.img = Image.new(
            'RGB',
            (self.width, self.height),
            bg
        )
        self.draw = ImageDraw.Draw(self.img)

    @staticmethod
    def font(size: int = 50):
        return ImageFont.truetype(f'fonts/capture-it.ttf', size=size)

    def draw_underline(self, text_coords: tuple, color: tuple) -> None:
        self.draw.line(
            (min(text_coords[0], text_coords[0]), text_coords[3] + 24,
             max(text_coords[2], text_coords[2]), text_coords[3] + 24),
            width=8, fill=color
        )

    def add_text(self, x: int, y: int, text: str, font: ImageFont, color: tuple = (255, 255, 255)) -> tuple:
        text_w, text_h = self.draw.textsize(text, font)
        xx, yy = x - text_w/2, y-text_h/2
        self.draw.text((xx, yy), text, font=font, fill=color)

        return xx, yy, xx + text_w, yy + text_h

    def save(self):
        self.img.save('image.png')