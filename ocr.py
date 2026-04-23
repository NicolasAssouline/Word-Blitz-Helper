import logging
import os

import cv2
import pytesseract

from env import IMAGES_DEBUG_OUTPUT_DIR, DEBUG_MODE

logger = logging.getLogger(__name__)

_replacements = {
	'°': 'O',
	'3': 'J',
	'1': 'I'
}


def extract_text_from_board(img):
	preprocessed_image = pre_process_image(img)
	if DEBUG_MODE:
		cv2.imwrite(os.path.join(IMAGES_DEBUG_OUTPUT_DIR, 'grid_mask.png'), preprocessed_image)

	text_boxes = find_text_boxes(preprocessed_image)
	if len(text_boxes) != 16:
		logger.warning(f'Cannot recognize board, try again ({len(text_boxes)} cells detected)')
		return None, None

	# must be done this way because the detected cells do not necessarily have the same y height
	# sort by rows
	columns = []
	for i in range(4):
		columns.append([])
		for cell in sorted(text_boxes, key=lambda cell: cell[1]):
			columns[-1].append(cell)
			if len(columns[-1]) == 4: break
		for cell in columns[-1]:
			text_boxes.remove(cell)

	# sort by columns
	for column in columns:
		column.sort(key=lambda col: col[0])

	characters_table, coordinates_table = [], []
	for i in range(len(columns)):
		characters_table.append([])
		coordinates_table.append([])
		for j in range(len(columns[i])):
			x, y, w, h = columns[i][j]

			# text detection works a bit better with padding
			x_start, x_end = x + 20, x + w - 15
			y_start, y_end = y, y + h

			image = img[y_start:y_end, x_start:x_end]

			if DEBUG_MODE:
				cv2.imwrite(os.path.join(IMAGES_DEBUG_OUTPUT_DIR, f'row_{i}_col_{j}.png'), image)

			# select the first one in case it detects more than one letter by accident
			characters_table[-1].append(pytesseract.image_to_string(image, config='--psm 10')[0].upper())
			coordinates_table[-1].append((int((x + 20 + x + w - 15)/2), int(y+h/2)))

	replace_common_mistakes(characters_table)
	return characters_table, coordinates_table


def replace_common_mistakes(final_table):
	for i in range(len(final_table)):
		for j in range(len(final_table[i])):
			if final_table[i][j] in _replacements:
				final_table[i][j] = _replacements[final_table[i][j]]


def pre_process_image(image, morph_size=(5, 5)):
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	image = cv2.threshold(image, 250, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, morph_size)
	return ~cv2.dilate(~image, kernel, anchor=(-1, -1), iterations=1)


def find_text_boxes(image, min_text_height_limit=40, max_text_height_limit=120):
	# Looking for the text spots contours
	contours, _ = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

	# Getting the texts bounding boxes based on the text size assumptions
	boxes = []
	for contour in contours:
		box = cv2.boundingRect(contour)

		height = box[3]
		if min_text_height_limit < height < max_text_height_limit:
			boxes.append(box)

	return boxes
