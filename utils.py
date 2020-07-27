import time

import numpy
import mss
import mss.tools
import cv2
from PIL import Image
import pytesseract

def take_screenshot(start, end):
	# image = pyautogui.screenshot(region=(
	# 	start.x(), start.y(),
	# 	end.x(), end.y()
	# ))
	with mss.mss() as sct:
		monitor_number = 1
		mon = sct.monitors[monitor_number]

		# The screen part to capture
		monitor = {
			"top": mon["top"] + start.x(),  # 100px from the top
			"left": mon["left"] + start.y(),  # 100px from the left
			"width": end.x() - start.x(),
			"height": end.y() - start.y(),
			"mon": monitor_number,
		}

		print(monitor)
		sct_img = sct.grab(monitor)
		image = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

	image = numpy.array(image)
	image = image[:, :, ::-1].copy()
	cv2.imshow('bla', image)
	analyze(image)

def analyze(image):
	img = cv2.imread('/home/nicolas/Pictures/Screenshot from 2020-07-25 13-28-10.png')
	# img = cv2.imread('/home/nicolas/Desktop/FAKS/MISC PROGRAMI/WORD_BLITZ_CHEAT/testocr.png')
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	cv2.imshow('bla', img)
	print('analyzing')
	text = pytesseract.image_to_string(img)
	print('len:', 2, '\t', text)
	time.sleep(2)

def analyze2():
	import os
	import cv2

