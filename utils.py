import time

import numpy
import mss
import mss.tools
import cv2
import pyautogui
from PIL import Image
import pytesseract

def take_screenshot(start, end):

	with mss.mss() as sct:
		monitor_number = 1

		if len(sct.monitors) <= 2:
			image = pyautogui.screenshot(region=(
				start.x(), start.y(),
				end.x()-start.x(), end.y()-start.y()
			))
		else:
			# todo fix multi monitor screenshots
			mon = sct.monitors[monitor_number]

			# The screen part to capture
			monitor = {
				"top": mon["top"] + start.x(),  # 100px from the top
				"left": mon["left"] + start.y(),  # 100px from the left
				"width": end.x() - start.x(),
				"height": end.y() - start.y(),
				"mon": monitor_number,
			}

			print('Screenshot using monitor', monitor)
			sct_img = sct.grab(monitor)

			image = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
	image = numpy.array(image)
	image = image[:, :, ::-1].copy()
	# cv2.imshow('screenshot', image)
	return image

def load_dictionary(dictionary_path='./dictionaries/corncob_caps.txt'):
	with open(dictionary_path) as file:
		return [word.strip() for word in file.readlines() if 1 < len(word.strip()) <= 16]