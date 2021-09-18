import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect, Qt, QSize
from PyQt5.QtGui import QPainter, QMouseEvent, QPaintEvent
from PyQt5.QtWidgets import QMainWindow, QApplication, QStyle, qApp

import utils
from ocr import *
from solver import solve_blitz
from utils import *


class MainWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		self.screenHeight = QtWidgets.qApp.primaryScreen().size().height()
		self.screenWidth = QtWidgets.qApp.primaryScreen().size().width()
		self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.X11BypassWindowManagerHint)

		self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignLeft, QSize(self.screenWidth, self.screenWidth), qApp.desktop().availableGeometry()))
		QMainWindow.setWindowOpacity(self, 0.5)

		self.mouse_start_pos = None
		self.mouse_curr_pos = None
		self.coords = None

	def mouseReleaseEvent(self, event: QMouseEvent) -> None:
		self.coords = (self.mouse_start_pos, self.mouse_curr_pos)

		self.mouse_start_pos = None
		self.mouse_curr_pos = None

	def mousePressEvent(self, event: QMouseEvent):
		if event.button() == 2:  # right click
			if self.coords is None or self.coords[0] is None: return
			self.window().close()

			print('Taking screenshot...')
			image = take_screenshot(self.coords[0], self.coords[1])

			print('Extracting text...')
			grid, coordinates = extract_text_from_board(image, verbose=True)
			if grid is None: return

			print('\nDetected grid:')
			for row in grid:
				for letter in row:
					print(letter, end=' ')
				print()

			print('Solving the blitz...\n')
			paths = solve_blitz(grid)

			for i in range(len(coordinates)):
				for j in range(len(coordinates[i])):
					coordinates[i][j] = (coordinates[i][j][0] + self.coords[0].x(),
										  coordinates[i][j][1] + self.coords[0].y())

			click_paths(coordinates, paths)

			QtWidgets.qApp.quit()

		if self.mouse_start_pos is None:
			self.mouse_start_pos = event.pos()
		self.update()

	def mouseMoveEvent(self, event: QMouseEvent) -> None:
		if self.mouse_start_pos is None:
			self.mouse_start_pos = event.pos()
		self.mouse_curr_pos = event.pos()
		self.update()

	def paintEvent(self, event: QPaintEvent) -> None:
		qp = QPainter()
		qp.begin(self)

		if self.mouse_start_pos is not None and self.mouse_curr_pos is not None:
			qp.drawRect(QRect(self.mouse_start_pos.x(), self.mouse_start_pos.y(),
							  self.mouse_curr_pos.x()-self.mouse_start_pos.x(),
							  self.mouse_curr_pos.y()-self.mouse_start_pos.y()))

			# print('start:', (self.mouse_start_pos.x(), self.mouse_start_pos.y()),
			# 	   '\tend:', (self.mouse_curr_pos.x(), self.mouse_curr_pos.y()))
		else:
			qp.eraseRect(0, 0, self.screenHeight, self.screenWidth)

		qp.end()

	def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
		print('Double click -> exiting')
		QtWidgets.qApp.quit()


if __name__ == '__main__':
	app = QApplication(sys.argv)

	print(utils.welcome_message)
	window = MainWindow()
	window.show()
	app.exec_()
