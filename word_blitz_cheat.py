from tkinter import *
from tkinter.ttk import *
import pyautogui, pyperclip, pyscreenshot
import time

class GUI:

	def __init__(self):
		# set up the UI
		self.root = Tk()
		# self.root.title('WORD BLITZ CHEAT by nikola')
		self.root.title('temp title')

		window_dimensions = (728, 524)
		self.root.minsize(*window_dimensions)
		self.root.maxsize(*window_dimensions)

		self.root.style = Style()
		self.root.style.theme_use('clam')
		GUI.__center__(self.root)

		def take_screenshot():
			clipboard_cache = pyperclip.paste()
			pyautogui.press(['shiftleft', 'ctrl', 'printscreen'])
			pyscreenshot.grab()
			clipboard_data = pyperclip.paste()
			print(clipboard_data)
			pyperclip.copy(clipboard_cache)

		btn_screenshot = Button(self.root, text='Take screenshot')
		btn_screenshot.pack(side='top', anchor='center')
		btn_screenshot.bind('<ButtonRelease-1>', lambda event: take_screenshot())

		canvas_img = Label(self.root, image=PhotoImage(file='/home/nicolas/Pictures/Screenshot from 2020-07-06 09-26-20.png').)
		canvas_img.pack(side='left', fill='x')


	@staticmethod
	def __center__(win: Tk):
		'''
		Centers the provided window to the center of the screen
		'''
		win.update_idletasks()
		width = win.winfo_width()
		height = win.winfo_height()

		# if width >= 1080*2: return

		x = (win.winfo_screenwidth() // 2) - (width // 2)
		y = (win.winfo_screenheight() // 2) - (height // 2)
		win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

	def show(self):
		self.root.mainloop()

if __name__ == '__main__':
	gui = GUI()
	gui.show()
