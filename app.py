import logging

from env import LOG_LEVEL
from ocr import extract_text_from_board
from utils import take_screenshot, grid_to_string, click_paths, welcome_message

import sys

from PyQt6.QtCore import QRect, Qt, QSize
from PyQt6.QtGui import QPainter, QMouseEvent, QPaintEvent
from PyQt6.QtWidgets import QMainWindow, QApplication, QStyle

from solver import solve_blitz

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		screen_size = QApplication.primaryScreen().size()
		self.screen_height = screen_size.height()
		self.screen_width = screen_size.width()
		self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint | Qt.WindowType.X11BypassWindowManagerHint)

		self.setGeometry(QStyle.alignedRect(Qt.LayoutDirection.LeftToRight, Qt.AlignmentFlag.AlignLeft, QSize(self.screen_width, self.screen_height), QApplication.primaryScreen().availableGeometry()))
		self.setWindowOpacity(0.5)

		self.mouse_start_pos = None
		self.mouse_curr_pos = None
		self.coords = None

	def mouseReleaseEvent(self, event: QMouseEvent) -> None:
		self.coords = (self.mouse_start_pos, self.mouse_curr_pos)

		self.mouse_start_pos = None
		self.mouse_curr_pos = None

	def mousePressEvent(self, event: QMouseEvent):
		if event.button() == Qt.MouseButton.RightButton:
			self._start_solver()
			QApplication.instance().quit()

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

			logger.debug(f'start: {(self.mouse_start_pos.x(), self.mouse_start_pos.y())}' +
						 f'\tend: {(self.mouse_curr_pos.x(), self.mouse_curr_pos.y())}')
		else:
			qp.eraseRect(0, 0, self.screen_width, self.screen_height)

		qp.end()

	def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
		logger.info('Double click -> exiting')
		QApplication.instance().quit()

	def _start_solver(self):
		if self.coords is None or self.coords[0] is None:
			logger.error('No coordinates selected')
			return
		self.window().close()

		logger.info('Taking screenshot...')
		image = take_screenshot(self.coords[0], self.coords[1])

		logger.info('Extracting text...')
		grid, coordinates = extract_text_from_board(image)
		if grid is None:
			return

		logger.info(f'Detected grid:\n{grid_to_string(grid)}')
		logger.info('Solving the blitz...')

		paths = solve_blitz(grid)

		for i in range(len(coordinates)):
			for j in range(len(coordinates[i])):
				coordinates[i][j] = (coordinates[i][j][0] + self.coords[0].x(),
				                     coordinates[i][j][1] + self.coords[0].y())

		click_paths(coordinates, paths)


if __name__ == '__main__':
	logging.basicConfig(level=LOG_LEVEL)
	app = QApplication(sys.argv)

	logger.info(welcome_message)
	window = MainWindow()
	window.show()
	app.exec()
