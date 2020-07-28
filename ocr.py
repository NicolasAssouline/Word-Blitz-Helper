import os

import cv2
import pytesseract

debug_output_dir = './debug_outputs'
if not os.path.exists(debug_output_dir): os.mkdir(debug_output_dir)

replacements = {
	'°': 'O'
}

def extract_text_from_board(img, debug=False):
	# img = cv2.imread(in_file)

	pre_processed = pre_process_image(img)
	if debug: cv2.imwrite(os.path.join(debug_output_dir, 'grid_mask.png'), pre_processed)

	text_boxes = find_text_boxes(pre_processed)
	if len(text_boxes) != 16:
		print('Cannot recognize board, try again, ({})'.format(len(text_boxes)))
		return None

	# must be done this way because the cells are not at the same y height
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

	final_table = []
	for i in range(len(columns)):
		final_table.append([])
		for j in range(len(columns[i])):
			x, y, w, h = columns[i][j]
			image = img[y:y + h, x + 20:x + w - 15]

			if debug:
				cv2.imwrite(os.path.join(debug_output_dir, 'row_{}_col_{}.png'.format(i, j)), image)

			# select the first one in case it detects more than one letter by accident
			final_table[-1].append(pytesseract.image_to_string(image, config='--psm 10')[0].upper())

	replace_common_mistakes(final_table)
	return final_table


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
