import os

import cv2
import pytesseract

debug_output_dir = './debug_outputs'

replacements = {
	'°': 'O',
	'3': 'J',
	'1': 'I'
}


def extract_text_from_board(img, verbose=False):
	pre_processed = pre_process_image(img)
	if verbose: cv2.imwrite(os.path.join(debug_output_dir, 'grid_mask.png'), pre_processed)

	text_boxes = find_text_boxes(pre_processed)
	if len(text_boxes) != 16:
		print('Cannot recognize board, try again, ({} cells detected)'.format(len(text_boxes)))
		return None

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

			# for parameter tuning
			x_start, x_end = x + 20, x + w - 15
			y_start, y_end = y, y + h

			image = img[y_start:y_end, x_start:x_end]

			if verbose:
				if not os.path.exists(debug_output_dir): os.mkdir(debug_output_dir)
				cv2.imwrite(os.path.join(debug_output_dir, 'row_{}_col_{}.png'.format(i, j)), image)

			# select the first one in case it detects more than one letter by accident
			characters_table[-1].append(pytesseract.image_to_string(image, config='--psm 10')[0].upper())
			coordinates_table[-1].append((int((x + 20 + x + w - 15)/2), int(y+h/2)))

	replace_common_mistakes(characters_table)
	return characters_table, coordinates_table


def replace_common_mistakes(final_table):
	for i in range(len(final_table)):
		for j in range(len(final_table[i])):
			if final_table[i][j] in replacements.keys():
				final_table[i][j] = replacements[final_table[i][j]]


def pre_process_image(img, morph_size=(5, 5)):
	# get rid of the color
	pre = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	pre = cv2.threshold(pre, 250, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	# dilate the text to make it solid spot
	cpy = pre.copy()
	struct = cv2.getStructuringElement(cv2.MORPH_RECT, morph_size)
	cpy = cv2.dilate(~cpy, struct, anchor=(-1, -1), iterations=1)
	return ~cpy


def find_text_boxes(pre, min_text_height_limit=40, max_text_height_limit=120):
	# Looking for the text spots contours
	contours, _ = cv2.findContours(pre, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

	# Getting the texts bounding boxes based on the text size assumptions
	boxes = []
	for contour in contours:
		box = cv2.boundingRect(contour)
		h = box[3]

		if min_text_height_limit < h < max_text_height_limit:
			boxes.append(box)

	return boxes
