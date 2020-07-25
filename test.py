import sys

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
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

		print('Done')


	def mousePressEvent(self, event):
		# painter = QPainter(self)
		# painter.setBrush()
		# painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
		# painter.drawLine(200, 200, 400, 400)
		self.update()

		print('mouseclick')
		# time.sleep(4)
		QtWidgets.qApp.quit()

	def paintEvent(self, event) -> None:
		qp = QPainter()
		qp.begin(self)
		# qp.drawLine(200, 200, 400, 400)
		qp.fillRect(100, 15, 800, 200, qp.brush())
		qp.drawRect(100, 15, 800, 600)
		qp.end()

		print('paintevent')
		# time.sleep(4)
		# QtWidgets.qApp.quit()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	mywindow = MainWindow()
	mywindow.show()
	app.exec_()