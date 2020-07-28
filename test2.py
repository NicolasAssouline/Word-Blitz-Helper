import os

import cv2
import pytesseract

from utils import analyze

# https://stackoverflow.com/questions/50829874/how-to-find-table-like-structure-in-image/51756462#51756462
# analyze(None)

# This only works if there's only one table on a page
# Important parameters:
#  - morph_size
#  - min_text_height_limit
#  - max_text_height_limit
#  - cell_threshold
#  - min_columns

def pre_process_image(img, morph_size=(23, 23)):
	# get rid of the color
	pre = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# Otsu threshold
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

if __name__ == "__main__":
	in_file = '/home/nicolas/Pictures/Screenshot from 2020-07-25 13-28-19.png'
	pre_file = 'pre.png'
	out_file = os.path.join(".", "out.png")

	img = cv2.imread(in_file)

	pre_processed = pre_process_image(img, pre_file)
	text_boxes = find_text_boxes(pre_processed)

	# Visualize the result
	vis = img.copy()

	cv2.imwrite('./out.png', vis)
	cells_copy = text_boxes.copy()


	# must be done this way because the cells are not at the same y height
	# sort by rows
	columns = []
	for i in range(4):
		columns.append([])
		for cell in sorted(cells_copy, key=lambda cell: cell[1]):
			columns[-1].append(cell)
			if len(columns[-1]) == 4: break
		for cell in columns[-1]:
			cells_copy.remove(cell)

	# sort by columns
	for column in columns:
		column.sort(key=lambda col: col[0])

	print('Detected board state:')
	final_table = []
	for col in columns:
		final_table.append([])
		for cell in col:
			x, y, w, h = cell
			image = img[y - 2:y + h, x + 20:x + w - 15]

			detected = pytesseract.image_to_string(image, config='--psm 10')[0] # in case it detects more than one letter by accident
			final_table[-1].append(detected)

			print(detected, end=' ')
		print()

	solve_blitz()

	# print('boxes:', len(text_boxes))
	# for i, cell in enumerate(text_boxes):
	# 	x, y, w, h = cell
	# 	image = vis[y-2:y + h, x+20:x + w-15]
	# 	cv2.imwrite('./bla{}.png'.format(i), image)
	# 	print(pytesseract.image_to_string(image, config='--psm 10'))

	# for box in text_boxes:
	# 	(x, y, w, h) = box
	# 	cv2.rectangle(vis, (x, y), (x + w - 2, y + h - 2), (0, 255, 0), 1)

	# for line in hor_lines:
	# 	[x1, y1, x2, y2] = line
	# 	cv2.line(vis, (x1, y1), (x2, y2), (0, 0, 255), 1)
	#
	# for line in ver_lines:
	# 	[x1, y1, x2, y2] = line
	# 	cv2.line(vis, (x1, y1), (x2, y2), (0, 0, 255), 1)

	# cv2.imwrite('./bla.png', img)
	# cv2.waitKey(0)