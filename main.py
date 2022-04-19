import datetime
import os
import time

from win32api import GetSystemMetrics
from utils import ImageBuilder, days, Exchange, change_wallpaper, Settings


if __name__ == '__main__':
    wei, hei = GetSystemMetrics(0), GetSystemMetrics(1)
    center_w, center_h = wei/2, hei/2

    theme = {'bg': (19, 19, 19), 'fg': (152, 0, 2), 'text': (255, 191, 0)}

    settings = Settings()
    current_m = -1
    while True:
        now_m = datetime.datetime.now().minute
        if current_m != now_m:
            print('Minute changed...')
            current_m = now_m

            image = ImageBuilder(wei, hei, bg=theme['bg'])
            today = days[datetime.datetime.today().isoweekday() - 1]
            today_coords = image.add_text(center_w, center_h - 100, today, ImageBuilder.font(85), color=theme['text'])

            exchange = Exchange(settings.get('exchange_api_url')).get()
            exchange_coords = image.add_text(center_w, center_h - 25, f"USD: {exchange['usd']:.2f}  EUR: {exchange['euro']:.2f}", ImageBuilder.font(45), color=theme['text'])

            image.draw_underline(text_coords=exchange_coords, color=theme['fg'])
            
            screen_time = datetime.datetime.now().strftime('%H:%M')
            screen_time_coords = image.add_text(center_w, center_h + 70, text=screen_time, font=ImageBuilder.font(85), color=theme['text'])

            date = datetime.datetime.now().strftime('%d.%m.%Y')
            date_coords = image.add_text(center_w, center_h + 150, text=date, font=ImageBuilder.font(45), color=theme['text'])

            image.save()
            change_wallpaper(os.getcwd() + "\\image.png")
        time.sleep(1)
