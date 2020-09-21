import time
from typing import List, Tuple

import mss
import mss.tools
import numpy
import pyautogui
from PIL import Image

welcome_message = """
|  |  __   __   __     __        ___ ___         __      __   __  __
|  | /  \ |__) |  \   |__) |   |  |   _/   |__| |_  |   |__) |_  |__)
|/\| \__/ | \  |__/   |__) |__ |  |  /__   |  | |__ |__ |    |__ | \ 
                                                                      
Usage:
Drag a rectangle around the word grid (approximately, doesn't have to be exact)
then right click to start the recognition process

Double click to exit the selection screen
"""


def click_paths(coordinates: List, paths: List[List[Tuple[int, int]]]):
    for path in reversed(paths):  # start from the longest word

        start = path.pop(0)
        pyautogui.moveTo(*coordinates[start[0]][start[1]], duration=0.1)
        print('moved cursor to ', *coordinates[start[0]][start[1]])

        pyautogui.mouseDown()
        for coords in path:
            pyautogui.moveTo(*coordinates[coords[0]][coords[1]], duration=0.1)
            print('moved cursor to ', *coordinates[coords[0]][coords[1]])

        pyautogui.mouseUp()
        time.sleep(0.1)


def take_screenshot(start, end):
    with mss.mss() as sct:
        monitor_number = 1

        if len(sct.monitors) <= 2:
            image = pyautogui.screenshot(region=(
                start.x(), start.y(),
                end.x() - start.x(), end.y() - start.y()
            ))
        else:
            # todo fix multi monitor screenshots
            mon = sct.monitors[monitor_number]

            # The screen part to capture
            monitor = {
                "top": mon["top"] + start.x(),
                "left": mon["left"] + start.y(),
                "width": end.x() - start.x(),
                "height": end.y() - start.y(),
                "mon": monitor_number,
            }

            print('Screenshot taken using monitor', monitor)
            sct_img = sct.grab(monitor)

            image = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
    image = numpy.array(image)
    image = image[:, :, ::-1].copy()
    # cv2.imshow('screenshot', image)
    return image


def load_dictionary(dictionary_path='./dictionaries/corncob_caps.txt'):
    with open(dictionary_path) as file:
        return [word.strip() for word in file.readlines() if 1 < len(word.strip()) <= 16 and not word.startswith('#')]
