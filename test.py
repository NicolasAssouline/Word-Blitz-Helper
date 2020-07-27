import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QRect
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtWidgets import QMainWindow, QApplication

import time

from utils import *

class MainWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		height = self.screen().size().height()
		width = self.screen().size().width()
		self.setWindowFlags(
			QtCore.Qt.WindowStaysOnTopHint |
			QtCore.Qt.FramelessWindowHint |
			QtCore.Qt.X11BypassWindowManagerHint
		)
		self.setGeometry(
			QtWidgets.QStyle.alignedRect(
				QtCore.Qt.LeftToRight, QtCore.Qt.AlignLeft,
				QtCore.QSize(width, height),
				QtWidgets.qApp.desktop().availableGeometry()
		))
		QMainWindow.setWindowOpacity(self, 0.5)

		self.mouse_start_pos = None
		self.mouse_curr_pos = None
		self.coords = None
		print('Done')

	def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
		self.coords = (self.mouse_start_pos, self.mouse_curr_pos)

		self.mouse_start_pos = None
		self.mouse_curr_pos = None

	def mousePressEvent(self, event: QtGui.QMouseEvent):
		if event.button() == 2: # desni klik
			# take_screenshot(self.coords[0], self.coords[1])
			analyze(None)
			return

		if self.mouse_start_pos is None:
			self.mouse_start_pos = event.pos()
		self.update()

	def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
		if self.mouse_start_pos is None:
			self.mouse_start_pos = event.pos()
		self.mouse_curr_pos = event.pos()
		self.update()

	def paintEvent(self, event: QtGui.QPaintEvent) -> None:
		qp = QPainter()
		qp.begin(self)

		if self.mouse_start_pos is not None and self.mouse_curr_pos is not None:
			qp.drawRect(QRect(self.mouse_start_pos.x(), self.mouse_start_pos.y(),
							  self.mouse_curr_pos.x()-self.mouse_start_pos.x(),
							  self.mouse_curr_pos.y()-self.mouse_start_pos.y()))

			print('start:', (self.mouse_start_pos.x(), self.mouse_start_pos.y()),
				   '\tend:', (self.mouse_curr_pos.x(), self.mouse_curr_pos.y()))
		else:
			qp.eraseRect(0, 0, self.screen().size().width(), self.screen().size().width())

		qp.end()

	def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent) -> None:
		print('Double click -> exiting')
		QtWidgets.qApp.quit()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec_()