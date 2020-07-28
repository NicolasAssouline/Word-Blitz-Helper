import os

import cv2
import pytesseract

from utils import analyze

# https://stackoverflow.com/questions/50829874/how-to-find-table-like-structure-in-image/51756462#51756462
# analyze(None)


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