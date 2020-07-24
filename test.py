import sys

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication


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
		QMainWindow.setWindowOpacity(self, 0.2)


	def mousePressEvent(self, event):
		QtWidgets.qApp.quit()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	mywindow = MainWindow()
	mywindow.show()
	app.exec_()