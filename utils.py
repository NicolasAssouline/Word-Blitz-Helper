import logging
import time
from typing import List, Tuple

import cv2
import numpy
import pyautogui
from pynput import keyboard

from env import DEFAULT_WORD_DICTIONARY, DEFAULT_PAUSE_BETWEEN_ACTIONS, DEBUG_MODE

logger = logging.getLogger(__name__)

welcome_message = """
|  |  __   __   __     __        ___ ___         __      __   __  __
|  | /  \ |__) |  \   |__) |   |  |   _/   |__| |_  |   |__) |_  |__)
|/\| \__/ | \  |__/   |__) |__ |  |  /__   |  | |__ |__ |    |__ | \ 
                                                                      
Usage:
Drag a rectangle around the word grid (approximately, doesn't have to be exact)
then right click to start the recognition process

Double click or press escape to exit the selection screen
To cancel the automatic solution input, press escape to terminate execution
"""


def click_paths(coordinates: List, paths: List[List[Tuple[int, int]]]):
    # disable qt app keyboard listeners so events don't get triggered recursively by the solver
    with keyboard.Listener(on_press=lambda key: False, on_release=lambda key: False) as listener:
        # start from the longest word
        for path in reversed(paths):

            start = path.pop(0)
            pyautogui.moveTo(*coordinates[start[0]][start[1]], duration=DEFAULT_PAUSE_BETWEEN_ACTIONS)
            logger.debug(f'Moved cursor to initial position {coordinates[start[0]][start[1]]}', )

            pyautogui.mouseDown()
            for coords in path:
                pyautogui.moveTo(*coordinates[coords[0]][coords[1]], duration=DEFAULT_PAUSE_BETWEEN_ACTIONS)

            pyautogui.mouseUp()
            time.sleep(DEFAULT_PAUSE_BETWEEN_ACTIONS)

            if not listener.running:
                logger.warning('Keyboard interrupt -> stopping execution...')
                return


def take_screenshot(start, end):
    image = pyautogui.screenshot(region=(
        start.x(), start.y(),
        end.x() - start.x(), end.y() - start.y()
    ))


    image = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)

    if DEBUG_MODE:
        cv2.imshow('screenshot', image)
    return image


def load_dictionary(dictionary_path=DEFAULT_WORD_DICTIONARY, max_word_length = 16):
    with open(dictionary_path) as file:
        return [word.strip() for word in file.readlines() if 1 < len(word.strip()) <= max_word_length and not word.startswith('#')]


def grid_to_string(grid: List[List[str]]) -> str:
    return '\n'.join(' '.join(row) for row in grid)