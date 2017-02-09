import Algorithms.Formulas as Formulas
from Utilities.Form import Form
from tkinter import Tk, X, LEFT, RIGHT, Spinbox, messagebox
from tkinter.ttk import Frame, Button, Label, Combobox


# /*\ =======================================================================
# |*|	START-GOAL PAIR SELECTOR
# |*|		- Opens a window with a dropdown list with different
# |*|		  start and goal locations
# \*/ =======================================================================
class StartGoalSelector(Form):
	def __init__(self, startList, goalList):
		super().__init__("Start-Goal Pair Selector", 320, 180)
		self.startList = startList
		self.index = -1

		# Information row
		infoRow = Frame(self)
		infoRow.pack(fill=X)
		heuristicLabel = Label(infoRow, text="Please select a start and goal pair.")
		heuristicLabel.config(font=("Calibri", 14))
		heuristicLabel.pack(side=LEFT, padx=30, pady=20)

		# Radio button row
		self.pairs = [None for x in range(10)]
		for i in range(len(startList)):
			self.pairs[i] = "".join(["Start: (", str(startList[i].X), ",", str(startList[i].Y), ") | Goal: (", str(goalList[i].X), ",", str(goalList[i].Y), ")"])

		startGoalRow = Frame(self)
		startGoalRow.pack(fill=X)
		self.combobox = Combobox(startGoalRow, state="readonly", values=self.pairs)
		self.combobox.bind("<<>ComboboxSelected>")
		self.combobox.set("".join(["Start: (", str(startList[0].X), ",", str(startList[0].Y), ") | Goal: (", str(goalList[0].X), ",", str(goalList[0].Y), ")"]))
		self.combobox.pack(fill=X, padx=(40, 40), expand=True)

		# Button row
		buttonRow = Frame(self)
		buttonRow.pack(fill="both")
		cancelButton = Button(buttonRow, text="Cancel", command=self.close)
		cancelButton.pack(side=RIGHT, padx=(0, 60), pady=(30, 0))
		selectButton = Button(buttonRow, text="Select", command=self.select)
		selectButton.pack(side=LEFT, padx=(60, 0), pady=(30, 0))

		# Run the main loop to show window
		self.root.mainloop()


	# Get the value from the combobox and return the index
	def select(self):
		for i in range(len(self.startList)):
			if(self.combobox.get() == self.pairs[i]):
				self.index = i

		# Close the box
		self.close()


# /*\ =======================================================================
# |*|	HEURISTIC SELECTOR
# |*|		- Opens a window with a dropdown list and a number entry text box
# |*|		  box. Can choose which heuristic the algorithm will run.
# \*/ =======================================================================
class HeuristicSelector(Form):
	# Reference var of window and list of heuristics
	heuristics = ['AStar Default', 'Manhattan Distance', 'Euclidean Distance', 'Chebyshev Distance', 'Diagonal Distance']

	# Construct the window
	def __init__(self):
		super().__init__("Heuristic Selector", 400, 200)
		self.weight = 0

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
		cancelButton.pack(side=RIGHT, padx=(0, 40), pady=(20, 0))
		selectButton = Button(buttonRow, text="Select", command=self.select)
		selectButton.pack(side=RIGHT, padx=(0, 0), pady=(20, 0))

		# Run the main loop to show window
		self.root.mainloop()


	# Get the values from the combobox and the text entry when user presses "Select"
	def select(self):
		if(self.combobox.get() == "AStar Default"):
			self.heuristic = Formulas.AStarHeuristic
		elif(self.combobox.get() == "Manhattan Distance"):
			self.heuristic = Formulas.ManhattanDistance
		elif(self.combobox.get() == "Euclidean Distance"):
			self.heuristic = Formulas.EuclideanDistance
		elif(self.combobox.get() == "Chebyshev Distance"):
			self.heuristic = Formulas.ChebyshevDistance
		elif(self.combobox.get() == "Diagonal Distance"):
			self.heuristic = Formulas.DiagonalDistance

		# Check if the weight is good
		try:
			self.weight = float(self.weightEntry.get())
			if(self.weight > 0):
				self.close()
			else:
				messagebox.showinfo("Weight Error", "Please enter a numeric value > 0 for the weight.")
		except:
			messagebox.showinfo("Weight Error", "Please enter a numeric value > 0 for the weight.")
