import time
import datetime

import win32api
import win32gui

from main import main

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

exit()
state_left = win32api.GetKeyState(
    0x01
)  # Left button down = 0 or 1. Button up = -127 or -128
print(state_left)
current_m = -1
while True:
    a = win32api.GetKeyState(0x01)
    now_m = datetime.datetime.now().minute
    if (a != state_left and a < 0) or current_m != now_m:  # Button state changed
        if a < 0:
            print("Left Button UP")
            time.sleep(0.01)
            focus = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            if focus in ('Program Manager', ''):
                x, y = win32api.GetCursorPos()
                print('FOCUS', x, y)
                time.sleep(0.01)
    time.sleep(0.02)
