from random import randrange, uniform
import tkinter as tk
from tkinter import filedialog

from Utilities import Constants
from Grid.Cell import Cell, Type, Point
from Grid.Highway import Highway


class Grid(Highway):
	# Static variables for saving and opening maps
	root = tk.Tk()
	root.withdraw()

	def __init__(self):
		# 2D array of cells
		self.cells = [[Cell(x, y) for y in range(Constants.COLUMNS)] for x in range(Constants.ROWS)]

		# Save the start, goal, and the eight hard to traverse centers
		self.startLocation = Point(0,0)
		self.goalLocation = Point(0,0)
		self.locations = [Point(0,0) for x in range(Constants.NUM_POINTS)]

		# Create the hard to traverse cells
		self.setHardToTraverse();

		# Create the highways
		self.setHighways()

		# Set the blocked, start, and goal cells
		self.setBlocked()

		print("\nStart and Goal Points:")
		self.setStartAndGoal()

		# Print new line
		print("")


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
							self.cells[row][col].type = Type.HARD


	# Create the highways
	def setHighways(self):
		for index in range(Constants.NUM_HIGHWAYS):
			highway = self.createHighway(self.cells)
			for point in highway:
				self.cells[point.x][point.y].isHighway = True


	# Choose 20% of the cells to be blocked
	def setBlocked(self):
		# Choose blocked cells
		blockedCells = 0
		while(blockedCells < (Constants.ROWS * Constants.COLUMNS) * 0.2):
			x = randrange(0, Constants.ROWS)
			y = randrange(0, Constants.COLUMNS)

			if(self.cells[x][y].isHighway == False):
				self.cells[x][y].type = Type.BLOCKED
				blockedCells += 1


	# Choose the start and goal cells
	def setStartAndGoal(self):
		found = False

		# Choose start vertex
		borderCells = self.getBorderCells()
		while found == False:
			index = randrange(0, len(borderCells))
			point = borderCells[index]

			if(self.cells[point.x][point.y].type != Type.BLOCKED):
				self.cells[point.x][point.y].isStart = True
				self.startLocation = point
				found = True

		# Choose goal vertex
		found = False
		while found == False:
			index = randrange(0, len(borderCells))
			point = borderCells[index]

			if(self.cells[point.x][point.y].type != Type.BLOCKED and point.distanceFrom(self.startLocation) > 100):
				self.cells[point.x][point.y].isGoal = True
				self.goalLocation = point
				found = True

		# Print the points out
		print("\t", self.startLocation.x, self.startLocation.y)
		print("\t", self.goalLocation.x, self.goalLocation.y)


	# Get border points
	def getBorderCells(self):
		borderCells = []

		for i in range(0, 20):							# Top 20 rows
			for j in range(0, Constants.COLUMNS):
				borderCells.append(Point(i, j))

		for i in range(99, Constants.ROWS):				# Bottom 20 rows
			for j in range(0, Constants.COLUMNS):
				borderCells.append(Point(i, j))

		for i in range(0, 20):							# Left-Most 20 columns
			for j in range(0, Constants.ROWS):
				borderCells.append(Point(j, i))

		for i in range(139, Constants.COLUMNS):			# Right-Most 20 columns
			for j in range(0, Constants.ROWS):
				borderCells.append(Point(j, i))

		return borderCells;


	# Saves the grid to a .map file
	def save(self):
		# Bring up save dialog box
		file = filedialog.asksaveasfilename(filetypes=[("Map files","*.map")], defaultextension=".map", initialdir = "Resources/maps")
		
		# Check if user clicked cancel
		if file is None:
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
					f.write(''.join(str(self.cells[row][col])))
				f.write('\n')

			f.close()
