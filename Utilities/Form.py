from tkinter import Tk, BOTH
from tkinter.ttk import Frame
from abc import ABC, abstractmethod

class Form(ABC, Frame):
  def __init__(self, title, width, height):
    self.root = Tk()
    self.root.protocol("WM_DELETE_WINDOW", self.close)
    Frame.__init__(self, self.root)

    # Window properties
    self.root.title(title)
    self.center_window(width, height)
    self.root.resizable(width=False, height=False)
    self.pack(fill=BOTH, expand=False)


  # Centers the window on the screen
  def center_window(self, width=400, height=200):
    # get screen width and height
    screen_width = self.root.winfo_screenwidth()
    screen_height = self.root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    self.root.geometry('%dx%d+%d+%d' % (width, height, x, y))


  # Close the window
  def close(self):
    self.root.quit()
    self.root.destroy()
