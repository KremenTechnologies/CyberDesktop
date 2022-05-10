import json
import os
import time
import locale
import psutil
import datetime
import win32api
import win32gui

from win32api import GetSystemMetrics
from utils import ImageBuilder, Exchange, change_wallpaper, Settings, Weather


class Theme:
    def __init__(self, settings: Settings, theme_id: int = 0):
        self.colors = settings.get("themes")[theme_id]


class Screen:
    def __init__(self):
        self.width, self.height = GetSystemMetrics(0), GetSystemMetrics(1)
        self.center_w, self.center_h = self.width / 2, self.height / 2


class Builder:
    def __init__(self):
        self.screen = Screen()
        self._reload_components(settings=True, theme=True)
        self.__set_locale()

    def _reload_components(self, settings: bool = False, theme: bool = False):
        if settings:
            self.settings = Settings()
            self.wallpaper_path = os.path.join(*self.settings.get("wallpaper_path"))
            self.__set_locale()
        if theme:
            self.theme = Theme(settings=self.settings, theme_id=0)
            self.image = ImageBuilder(self.screen.width, self.screen.height, bg=self.theme.colors["bg"])

    def __set_locale(self):
        locale_lang = self.settings.get("locale")
        locale.setlocale(locale.LC_ALL, f"{locale_lang}.UTF-8")

    def __build(self):
        self.image.save(image=self.wallpaper_path)
        change_wallpaper(self.wallpaper_path)


def main():
    width, height = GetSystemMetrics(0), GetSystemMetrics(1)
    center_w, center_h = width / 2, height / 2
    theme = {"bg": (19, 19, 19), "fg": (152, 0, 2), "text": (255, 191, 0)}

    settings = Settings()

    locale_lang = settings.get("locale")
    locale.setlocale(locale.LC_ALL, f"{locale_lang}.UTF-8")

    current_m = -1
    while True:
        now_m = datetime.datetime.now().minute
        if current_m != now_m:
            print("Minute changed...")
            current_m = now_m
            image = ImageBuilder(width, height, bg=theme["bg"])

            # Top center block
            weather_settings = settings.get("weather_api")
            weather = Weather(
                city_id=weather_settings["city_id"],
                api_key=weather_settings["token"],
                locale=locale_lang,
            ).get()
            if weather:
                weather_city_coords = image.add_text(
                    center_w,
                    20,
                    f"{weather['city']}",
                    color=theme["text"],
                    font=ImageBuilder.font(35),
                )
                weather_coords = image.add_text(
                    center_w,
                    weather_city_coords[3] + 20,
                    f"{int(weather['temp'])}'c | {weather['weather']} | {weather['wind']}м/с",
                    color=theme["text"],
                    font=ImageBuilder.font(24),
                )
            # Top center block

            # Center Block
            center_block_y_offset = -75
            today = datetime.datetime.now().strftime("%A")
            today_coords = image.add_text(
                center_w,
                center_h - 100 + center_block_y_offset,
                today,
                ImageBuilder.font(85),
                color=theme["text"],
            )

            underline_coord = today_coords
            exchange = Exchange().get()
            if exchange:
                exchange_coords = image.add_text(
                    center_w,
                    center_h - 25 + center_block_y_offset,
                    f"USD: {exchange['usd']:.2f}  EUR: {exchange['euro']:.2f}",
                    ImageBuilder.font(45),
                    color=theme["text"],
                )
                underline_coord = exchange_coords

            image.draw_underline(text_coords=underline_coord, color=theme["fg"])

            screen_time = datetime.datetime.now().strftime("%H:%M")
            screen_time_coords = image.add_text(
                center_w,
                center_h + 60 + center_block_y_offset,
                text=screen_time,
                font=ImageBuilder.font(85),
                color=theme["text"],
            )

            date = datetime.datetime.now().strftime("%d.%m.%Y")
            date_coords = image.add_text(
                center_w,
                center_h + 125 + center_block_y_offset,
                text=date,
                font=ImageBuilder.font(45),
                color=theme["text"],
            )
            # Center Block

            # Bottom Center Block
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory()
            str_ram = f"CPU: {cpu}% | RAM: {(ram[3]/1024/1024/1024):.1f}/{ram[0]/1024/1024/1024:.1f} GB | {ram[2]}%"
            stat_coords = image.add_text(
                center_w,
                height - 60,
                text=str_ram,
                font=ImageBuilder.font(24),
                color=theme["text"],
            )
            # Bottom Center Block

            # # Right block
            # current_lang = locale_lang.split("_")[0].upper()
            # change_style_btn = image.add_text(
            #     width - 5 - image.get_text_size(text=current_lang, font=ImageBuilder.font(24))[0],
            #     height - 60,
            #     text=current_lang,
            #     font=ImageBuilder.font(24),
            #     color=theme["text"],
            #     in_box=True,
            #     in_box_padding=6
            # )
            # # Right block
            # xxx = width - 5 - image.get_text_size(text=current_lang, font=ImageBuilder.font(24))[0]
            # yyy = height - 60
            # print(in_coords(xy=(width, height), box=change_style_btn[4]))
            # SAVE AND APPLY
            relative_image_path = "resources\\wallpaper\\image.png"

            image.save(image=relative_image_path)
            change_wallpaper(os.getcwd() + "\\" + relative_image_path)

        time.sleep(1)


if __name__ == "__main__":
    main()

exit()
# Future update logic

pressed = False
used = False
current_m = -1

while True:
    now_m = datetime.datetime.now().minute
    if win32api.GetKeyState(0x01) < -1 and not pressed:
        pressed = True
        print('CLICK DOWN ', pressed, win32api.GetKeyState(0x01))
    elif win32api.GetKeyState(0x01) > -1 and pressed:
        pressed = False
        used = False
        print('CLICK UP ', pressed, win32api.GetKeyState(0x01))

    new_click_up = not pressed and not used
    new_minute = current_m != now_m

    if new_minute:
        main()  # UPDATE IMAGE

    if new_click_up:
        used = True

        focus = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        if focus in ('Program Manager', ''):
            x, y = win32api.GetCursorPos()
            print('FOCUS', x, y)

            # main()  # UPDATE IMAGE
            time.sleep(0.01)

    time.sleep(0.01)