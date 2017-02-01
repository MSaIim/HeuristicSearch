import numpy as np
import tkinter as tk
from tkinter import filedialog
from random import randrange, uniform
import Utilities.Constants as Constants
from Grid.Cell import Cell, Type, Point
from Grid.Highway import Highway


class Grid(Highway):
	# Static variables for saving and opening maps
	root = tk.Tk()
	root.withdraw()

	def __init__(self):
		# 2D array of cells
		self.cells = np.asmatrix([[Cell(x, y) for y in range(Constants.COLUMNS)] for x in range(Constants.ROWS)])

		# Save the start, goal, and the eight hard to traverse centers
		self.startLocation = Cell(-1, -1)
		self.goalLocation = Cell(-1, -1)
		self.locations = np.array([Point(0,0) for x in range(Constants.NUM_POINTS)])

		# Create the different types of cells
		self.setHardToTraverse();
		self.setHighways()
		self.setBlocked()
		self.setStartAndGoal()


	# Choose random centers and mark hard to traverse cells around a 31x31 area
	def setHardToTraverse(self):
		# Choose 8 random coordinates
		index = 0
		while(index < Constants.NUM_POINTS):
			temp = Point(randrange(0, Constants.ROWS-1), randrange(0, Constants.COLUMNS-1))
			if(temp not in self.locations):
				self.locations[index] = temp
				index += 1

		# 50% probability to make a cell HARD TO TRAVERSE around the coordinates chosen above
		for location in self.locations:
			for row in range(location.x - 15, location.x + 15):
				for col in range(location.y - 15, location.y + 15):
					if(row > -1 and row < Constants.ROWS and col > -1 and col < Constants.COLUMNS):
						if(uniform(0, 1) > 0.49):
							self.cells[row, col].type = Type.HARD


	# Create the highways
	def setHighways(self):
		for index in range(Constants.NUM_HIGHWAYS):
			highway = self.createHighway(self.cells)
			for point in highway:
				self.cells[point.x, point.y].isHighway = True


	# Choose 20% of the cells to be blocked
	def setBlocked(self):
		# Choose blocked cells
		blockedCells = 0
		while(blockedCells < (Constants.ROWS * Constants.COLUMNS) * 0.2):
			x = randrange(0, Constants.ROWS)
			y = randrange(0, Constants.COLUMNS)

			if(self.cells[x, y].isHighway == False):
				self.cells[x, y].type = Type.BLOCKED
				blockedCells += 1


	# Choose the start and goal cells
	def setStartAndGoal(self):
		found = False

		# Choose start vertex
		borderCells = self.getBorderCells()
		while found == False:
			index = randrange(0, len(borderCells))
			point = borderCells[index]

			if(self.cells[point.x, point.y].type != Type.BLOCKED):
				self.cells[point.x, point.y].isStart = True
				start = point
				found = True

		# Choose goal vertex
		found = False
		while found == False:
			index = randrange(0, len(borderCells))
			point = borderCells[index]

			if(self.cells[point.x, point.y].type != Type.BLOCKED and point.distanceFrom(start) > 100):
				self.cells[point.x, point.y].isGoal = True
				goal = point
				found = True

		# Set start and goal
		self.startLocation = self.cells[start.x, start.y]
		self.goalLocation = self.cells[goal.x, goal.y]


	# Get border points
	def getBorderCells(self):
		borderCells = []
		append = borderCells.append

		for i in range(0, 20):							# Top 20 rows
			for j in range(0, Constants.COLUMNS):
				append(Point(i, j))

		for i in range(99, Constants.ROWS):				# Bottom 20 rows
			for j in range(0, Constants.COLUMNS):
				append(Point(i, j))

		for i in range(0, 20):							# Left-Most 20 columns
			for j in range(0, Constants.ROWS):
				append(Point(j, i))

		for i in range(139, Constants.COLUMNS):			# Right-Most 20 columns
			for j in range(0, Constants.ROWS):
				append(Point(j, i))

		return borderCells;


	def setPath(self, path):
		if(path != None):
			for index in range(len(path)):
				if(path[index] != self.startLocation and path[index] != self.goalLocation):
					self.cells[path[index].X, path[index].Y].isPath = True


	# Saves the grid to a .map file
	def save(self):
		# Bring up save dialog box
		file = filedialog.asksaveasfilename(filetypes=[("Map files","*.map")], defaultextension=".map", initialdir = "Resources/maps")
		
		# Check if user clicked cancel
		if file is None or file is '':
			return False

		# Write to file
		with open(file, 'w') as f:
			# Start and Goal locations on first two lines
			f.write("".join([str(self.startLocation), '\n', str(self.goalLocation), '\n']))

			# The eight hard-to-traverse center points
			f.write('\n'.join(str(point) for point in self.locations))
			f.write('\n')

			# The actual grid (160 characters per line)
			for row in range(Constants.ROWS):
				for col in range(Constants.COLUMNS):
					f.write(''.join(str(self.cells[row, col])))
				f.write('\n')

			f.close()

		return True


	# Saves the grid to a .map file
	def load(self):
		# Bring up save dialog box
		file = filedialog.askopenfilename(filetypes=[("Map files","*.map")], initialdir = "Resources/maps")

		# Check if user clicked cancel
		if file is None or file is '':
			return False

		# Write to file
		with open(file, 'r') as f:
			index = 0
			lines = f.read().split("\n")
			start = lines[0]
			goal = lines[1]
			lines = lines[10:]
			characters = [list(line) for line in lines]

			for row in range(Constants.ROWS):
				for col in range(Constants.COLUMNS):
					if(characters[row][col] == '0'):
						self.cells[row, col] = Cell(row, col)
						self.cells[row, col].type = Type.BLOCKED
					elif(characters[row][col] == 'a'):
						self.cells[row, col] = Cell(row, col)
						self.cells[row, col].type = Type.REGULAR
						self.cells[row, col].isHighway = True
					elif(characters[row][col] == 'b'):
						self.cells[row, col] = Cell(row, col)
						self.cells[row, col].type = Type.HARD
						self.cells[row, col].isHighway = True
					elif(characters[row][col] == '1'):
						self.cells[row, col] = Cell(row, col)
						self.cells[row, col].type = Type.REGULAR
					elif(characters[row][col] == '2'):
						self.cells[row, col] = Cell(row, col)
						self.cells[row, col].type = Type.HARD

			a, b = eval(start)
			c, d = eval(goal)
			x1, y1 = int(a), int(b)
			x2, y2 = int(c), int(d)
			self.cells[a, b].isStart = True
			self.cells[c, d].isGoal = True
			self.startLocation = self.cells[a, b]
			self.goalLocation = self.cells[c, d]
			f.close()
