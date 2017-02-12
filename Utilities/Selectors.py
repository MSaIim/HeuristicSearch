import Algorithms.Base.Formulas as Formulas
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
class WeightedSelector(Form):
	# Reference var of window and list of heuristics
	heuristics = ['AStar Default', 'Manhattan Distance', 'Euclidean Distance', 'Chebyshev Distance', 'Diagonal Distance']

	# Construct the window
	def __init__(self):
		super().__init__("Weighted A* Setup", 400, 200)
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
		self.combobox.bind("<<ComboboxSelected>>")
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
		selectButton = Button(buttonRow, text="Submit", command=self.submit)
		selectButton.pack(side=RIGHT, padx=(0, 0), pady=(20, 0))

		# Run the main loop to show window
		self.root.mainloop()


	# Get the values from the combobox and the text entry when user presses "Select"
	def submit(self):
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
			if(self.weight >= 1):
				self.close()
			else:
				messagebox.showinfo("Weight Error", "Please enter a numeric value > 0 for the weight.")
		except:
			messagebox.showinfo("Weight Error", "Please enter a numeric value > 0 for the weight.")


# /*\ =======================================================================
# |*|	SEQUENTIAL HEURISTIC SELECTOR
# |*|		- Opens a window with dropdown lists for the anchor heuristic
# |*|         and the other four the user may choose from. In addition,
# |*|         two weights can be chosen.
# \*/ =======================================================================
class SequentialSelector(Form):
	anchors = ['Manhattan Distance', 'Euclidean Distance']
	heuristics = ['None', 'AStar (Given Heuristic)', 'Euclidean Distance', 'Chebyshev Distance', 'Diagonal Distance']

	# Construct the window
	def __init__(self):
		super().__init__("Sequential A* Setup", 400, 350)
		self.weight1 = 0
		self.weight2 = 0

		# Information row
		infoRow = Frame(self)
		infoRow.pack(fill=X)
		infoLabel = Label(infoRow, text="Select anchor, other heuristics, and two weights.")
		infoLabel.config(font=("Calibri", 12))
		infoLabel.pack(side=LEFT, padx=(35, 0), pady=20)

		# Anchor row
		anchorRow = Frame(self)
		anchorRow.pack(fill=X)
		anchorLabel = Label(anchorRow, text="Anchor:")
		anchorLabel.pack(side=LEFT, padx=(30, 10), pady=5)
		self.anchorBox = Combobox(anchorRow, state="readonly", values=self.anchors)
		self.anchorBox.bind("<<ComboboxSelected>>", self.onChangeAnchor)
		self.anchorBox.set("Manhattan Distance")
		self.anchorBox.pack(fill=X, padx=(0, 30), expand=True)

		# Heuristic Selector Label
		heuLabelRow = Frame(self)
		heuLabelRow.pack(fill=X)
		heuristicLabel = Label(heuLabelRow, text="Heuristics (Duplicates will be discarded):")
		heuristicLabel.pack(side=LEFT, padx=(30, 10), pady=(20, 5))

		# Heuristic 1-2
		heuristicRow1 = Frame(self)
		heuristicRow1.pack(fill=X)
		self.heuristicBox1 = Combobox(heuristicRow1, state="readonly", values=self.heuristics)
		self.heuristicBox1.bind("<<ComboboxSelected>>")
		self.heuristicBox1.set("None")
		self.heuristicBox1.pack(side=LEFT, padx=(30,0))

		self.heuristicBox2 = Combobox(heuristicRow1, state="readonly", values=self.heuristics)
		self.heuristicBox2.bind("<<ComboboxSelected>>")
		self.heuristicBox2.set("None")
		self.heuristicBox2.pack(side=RIGHT, padx=(0,30))

		# Heuristic 3-4
		heuristicRow2 = Frame(self)
		heuristicRow2.pack(fill=X)
		self.heuristicBox3 = Combobox(heuristicRow2, state="readonly", values=self.heuristics)
		self.heuristicBox3.bind("<<ComboboxSelected>>")
		self.heuristicBox3.set("None")
		self.heuristicBox3.pack(side=LEFT, padx=(30,0), pady=(5, 0))

		self.heuristicBox4 = Combobox(heuristicRow2, state="readonly", values=self.heuristics)
		self.heuristicBox4.bind("<<ComboboxSelected>>")
		self.heuristicBox4.set("None")
		self.heuristicBox4.pack(side=RIGHT, padx=(0,30), pady=(5, 0))

		# Weight label row
		weightLabelRow = Frame(self)
		weightLabelRow.pack(fill=X)
		weightLabel = Label(weightLabelRow, text="Please enter two weights:")
		weightLabel.pack(side=LEFT, padx=(30,0), pady=(20, 5))

		# Weight entry row 1
		weightRow1 = Frame(self)
		weightRow1.pack(fill=X)
		self.weightEntry1 = Spinbox(weightRow1, from_=1, to=9999)
		self.weightEntry1.pack(fill=X, padx=(30,30), expand=True)

		# Weight entry row 2
		weightRow2 = Frame(self)
		weightRow2.pack(fill=X)
		self.weightEntry2 = Spinbox(weightRow2, from_=1, to=9999)
		self.weightEntry2.pack(fill=X, padx=(30,30), pady=(5,0), expand=True)

		# Button row
		buttonRow = Frame(self)
		buttonRow.pack(fill=X)
		cancelButton = Button(buttonRow, text="Cancel", command=self.close)
		cancelButton.pack(side=RIGHT, padx=(0, 30), pady=(25, 0))
		selectButton = Button(buttonRow, text="Submit", command=self.submit)
		selectButton.pack(side=RIGHT, padx=(0, 0), pady=(25, 0))

		# Run the main loop to show window
		self.root.mainloop()


	# Selection event for anchor
	def onChangeAnchor(self, event):
		if(self.anchorBox.get() == "Manhattan Distance"):
			self.heuristics = ['None', 'AStar (Given Heuristic)', 'Euclidean Distance', 'Chebyshev Distance', 'Diagonal Distance']
			self.heuristicBox1['values'] = self.heuristics
			self.heuristicBox2['values'] = self.heuristics
			self.heuristicBox3['values'] = self.heuristics
			self.heuristicBox4['values'] = self.heuristics

			if(self.heuristicBox1.get() == "Manhattan Distance"):
				self.heuristicBox1.set("None")
			if(self.heuristicBox2.get() == "Manhattan Distance"):
				self.heuristicBox2.set("None")
			if(self.heuristicBox3.get() == "Manhattan Distance"):
				self.heuristicBox3.set("None")
			if(self.heuristicBox4.get() == "Manhattan Distance"):
				self.heuristicBox4.set("None")

		elif(self.anchorBox.get() == "Euclidean Distance"):
			self.heuristics = ['None', 'AStar (Given Heuristic)', 'Manhattan Distance', 'Chebyshev Distance', 'Diagonal Distance']
			self.heuristicBox1['values'] = self.heuristics
			self.heuristicBox2['values'] = self.heuristics
			self.heuristicBox3['values'] = self.heuristics
			self.heuristicBox4['values'] = self.heuristics

			if(self.heuristicBox1.get() == "Euclidean Distance"):
				self.heuristicBox1.set("None")
			if(self.heuristicBox2.get() == "Euclidean Distance"):
				self.heuristicBox2.set("None")
			if(self.heuristicBox3.get() == "Euclidean Distance"):
				self.heuristicBox3.set("None")
			if(self.heuristicBox4.get() == "Euclidean Distance"):
				self.heuristicBox4.set("None")


	# Get the values from the combobox and the text entry when user presses "Select"
	def submit(self):
		# Make a dictionary with anchor and the selected heuristics
		heuDict = {'Anchor': self.anchorBox.get()}
		valueList = set([self.heuristicBox1.get(), self.heuristicBox2.get(), self.heuristicBox3.get(), self.heuristicBox4.get()])
		valueList.discard("None")

		# Check if at least 1 heuristic is selected
		if(len(valueList) > 0):
			heuDict['Heuristics'] = valueList
			
			# Iterate over heuristics and add to list
			heuristicList = [heuDict['Anchor']]
			for i in range(len(heuDict['Heuristics'])):
				heuristicList.append(heuDict['Heuristics'].pop())

			# Get the function pointers
			self.heuristicFunctions = []
			for i in range(len(heuristicList)):
				if(heuristicList[i] == "Manhattan Distance"):
					self.heuristicFunctions.append(Formulas.ManhattanDistance)
				elif(heuristicList[i] == "Euclidean Distance"):
					self.heuristicFunctions.append(Formulas.EuclideanDistance)
				elif(heuristicList[i] == "AStar (Given Heuristic)"):
					self.heuristicFunctions.append(Formulas.AStarHeuristic)
				elif(heuristicList[i] == "Chebyshev Distance"):
					self.heuristicFunctions.append(Formulas.ChebyshevDistance)
				elif(heuristicList[i] == "Diagonal Distance"):
					self.heuristicFunctions.append(Formulas.DiagonalDistance)

			# Check if the weights are good
			try:
				self.weight1 = float(self.weightEntry1.get())
				self.weight2 = float(self.weightEntry2.get())

				if(self.weight1 >= 1 and self.weight2 >= 1):
					self.close()
				else:
					messagebox.showinfo("Weight Error", "Please enter a numeric value > 0 for the weights.")
			except:
				messagebox.showinfo("Weight Error", "Please enter a numeric value > 0 for the weights.")

		# Heuristics not chosen
		else:
			messagebox.showinfo("Heuristic Error", "Please choose at least one heuristic.")
