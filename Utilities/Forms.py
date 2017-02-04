import Algorithms.Formulas as Formulas
from tkinter import Tk, BOTH, X, LEFT, RIGHT, Spinbox, messagebox
from tkinter.ttk import Frame, Combobox, Button, Label

class HeuristicSelector(Frame):
	# Reference var of window and list of heuristics
	heuristics = ['AStar Default', 'Manhattan Distance', 'Euclidean Distance', 'Euclidean Distance Squared']

	# Construct the window
	def __init__(self):
		self.root = Tk()
		self.weight = 0
		self.root.protocol("WM_DELETE_WINDOW", self.close)
		Frame.__init__(self, self.root)

		# Window properties
		self.root.title("Heuristic Selector")
		self.center_window(400, 180)
		self.root.resizable(width=False, height=False)
		self.pack(fill=BOTH, expand=False)

		# Information row
		infoRow = Frame(self)
		infoRow.pack(fill=X)
		heuristicLabel = Label(infoRow, text="     Please select a heuristic and a weight.")
		heuristicLabel.config(font=("Calibri", 14))
		heuristicLabel.pack(side=LEFT, padx=30, pady=20)

		# Heuristic row
		heuristicRow = Frame(self)
		heuristicRow.pack(fill=X)
		heuristicLabel = Label(heuristicRow, text="Heuristics:")
		heuristicLabel.pack(side=LEFT, padx=(30, 10), pady=5)
		self.combobox = Combobox(heuristicRow, state="readonly", values=self.heuristics)
		self.combobox.bind("<<>ComboboxSelected>")
		self.combobox.set("Manhattan Distance")
		self.combobox.pack(fill=X, padx=(0, 40), expand=True)

		# Weight row
		weightRow = Frame(self)
		weightRow.pack(fill=X)
		heuristicLabel = Label(weightRow, text="Weight:")
		heuristicLabel.pack(side=LEFT, padx=(30, 20), pady=5)
		self.weightEntry = Spinbox(weightRow, from_=1, to=9999)
		self.weightEntry.pack(fill=X, padx=(4, 40), expand=True)

		# Button row
		buttonRow = Frame(self)
		buttonRow.pack(fill=X)
		cancelButton = Button(buttonRow, text="Cancel", command=self.close)
		cancelButton.pack(side=RIGHT, padx=(0, 40), pady=10)
		selectButton = Button(buttonRow, text="Select", command=self.select)
		selectButton.pack(side=RIGHT)

		# Run the main loop to show window
		self.root.mainloop()


	# Centers the window on the screen
	def center_window(self, width=400, height=200):
		# get screen width and height
		screen_width = self.root.winfo_screenwidth()
		screen_height = self.root.winfo_screenheight()

		# calculate position x and y coordinates
		x = (screen_width/2) - (width/2)
		y = (screen_height/2) - (height/2)
		self.root.geometry('%dx%d+%d+%d' % (width, height, x, y))


	# Get the values from the combobox and the text entry when user presses "Select"
	def select(self):
		if(self.combobox.get() == "AStar Default"):
			self.heuristic = Formulas.AStarHeuristic
		elif(self.combobox.get() == "Manhattan Distance"):
			self.heuristic = Formulas.ManhattanDistance
		elif(self.combobox.get() == "Euclidean Distance"):
			self.heuristic = Formulas.EuclideanDistance
		elif(self.combobox.get() == "Euclidean Distance Squared"):
			self.heuristic = Formulas.EuclideanDistanceSquared

		# Check if the weight is good
		try:
			self.weight = float(self.weightEntry.get())
			if(self.weight > 0):
				self.close()
			else:
				messagebox.showinfo("Weight Error", "Please enter a numeric value > 1 for the weight.")
		except:
			messagebox.showinfo("Weight Error", "Please enter a numeric value > 1 for the weight.")


	# Close the window
	def close(self):
		self.root.quit()
		self.root.destroy()
