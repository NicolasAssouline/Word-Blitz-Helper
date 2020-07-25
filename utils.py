import numpy
import mss
import cv2

def take_screenshot(start, end):
	image = pyautogui.screenshot(region=(
		start.x(), start.y(),
		end.x(), end.y()
	))
	image = numpy.array(image)
	image = image[:, :, ::-1].copy()
	cv2.imshow('bla', image)