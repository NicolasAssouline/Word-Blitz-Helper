import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QRect
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtWidgets import QMainWindow, QApplication

import time

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
		print('Done')

	def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
		self.mouse_start_pos = None
		QtWidgets.qApp.quit()

	def mousePressEvent(self, event: QtGui.QMouseEvent):
		if self.mouse_start_pos is None:
			self.mouse_start_pos = event.pos()


		# painter = QPainter(self)
		# painter.setBrush()
		# painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
		# painter.drawLine(200, 200, 400, 400)
		self.update()

		print('mouseclick')
		# time.sleep(4)
		# QtWidgets.qApp.quit()

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
							  # self.mouse_start_pos.x()+1, self.mouse_start_pos.y()+1))
							  self.mouse_curr_pos.x()-self.mouse_start_pos.x(),
							  self.mouse_curr_pos.y()-self.mouse_start_pos.y()))

			print(self.mouse_start_pos.x(), self.mouse_start_pos.y(),
				   self.mouse_curr_pos.x(), self.mouse_curr_pos.y())
		qp.end()


		# print('paintevent')
		# time.sleep(4)
		# QtWidgets.qApp.quit()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	mywindow = MainWindow()
	mywindow.show()
	app.exec_()