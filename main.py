import datetime
import locale
import os
import time
import psutil

from win32api import GetSystemMetrics
from utils import ImageBuilder, Exchange, change_wallpaper, Settings, Weather

if __name__ == "__main__":
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
            relative_image_path = "resources\\wallpaper\\image.png"

            image.save(image=relative_image_path)
            change_wallpaper(os.getcwd() + "\\" + relative_image_path)

        time.sleep(1)
