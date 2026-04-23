import os
from datetime import timedelta
import logging

LOG_LEVEL = logging.INFO
DEBUG_MODE = LOG_LEVEL == logging.DEBUG

DEFAULT_WORD_DICTIONARY='./dictionaries/corncob_caps.txt'
DEFAULT_PAUSE_BETWEEN_ACTIONS = timedelta(seconds=0.1).total_seconds()

IMAGES_DEBUG_OUTPUT_DIR = './debug_outputs'
if DEBUG_MODE and not os.path.exists(IMAGES_DEBUG_OUTPUT_DIR):
    os.mkdir(IMAGES_DEBUG_OUTPUT_DIR)
