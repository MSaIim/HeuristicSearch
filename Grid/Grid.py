import re
import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from random import randrange, uniform
import Utilities.Constants as Constants
from Grid.Cell import Cell, Type, Direction, Point


class Grid(object):
	# Static variables for saving and opening maps
	root = tk.Tk()
	root.withdraw()

	def __init__(self):
		# 2D array of cells
		full_width, full_height = Constants.MARGIN + Constants.WIDTH, Constants.MARGIN + Constants.HEIGHT

		self.cells = np.asmatrix(
			[[Cell(x, y, [full_width * y + Constants.MARGIN, full_height * x + Constants.MARGIN, Constants.WIDTH, Constants.HEIGHT]) 
			for y in range(Constants.COLUMNS)] 
			for x in range(Constants.ROWS)])

		# Save the start, goal, and the eight hard to traverse centers
		self.startLocations = []
		self.goalLocations = []
		self.currentStart = None
		self.currentGoal = None
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
		# Get border cells
		borderCells = self.getBorderCells()

		# Choose 10 start cells
		for i in range(10):
			found = False
			while found == False:
				index = randrange(0, len(borderCells))
				point = borderCells[index]

				if(self.cells[point.x, point.y].type != Type.BLOCKED):
					self.startLocations.append(self.cells[point.x, point.y])
					found = True

		# Choose goal vertex
		for i in range(10):
			found = False
			while found == False:
				index = randrange(0, len(borderCells))
				point = borderCells[index]

				if(self.cells[point.x, point.y].type != Type.BLOCKED and self.cells[point.x, point.y] not in self.startLocations):
					if(point.distanceFrom(Point(self.startLocations[i].X, self.startLocations[i].Y)) > 100):
						self.goalLocations.append(self.cells[point.x, point.y])
						found = True

		# Set start and goal
		self.startLocations[0].isStart = True
		self.goalLocations[0].isGoal = True
		self.currentStart = self.startLocations[0]
		self.currentGoal = self.goalLocations[0]


	# Get a good high way
	def createHighway(self, gridCells):
		self.cells = gridCells

		# Loop until a good highway is formed
		done = False
		while done == False:
			coord = self.getBoundaryPoint()			# Get a random border point
			highway = self.getHighway(coord)		# Get a list of points
			if(len(highway) >= 100):				# Check if highway is good
				done = True

		# Return good highway
		return highway


	# Get the highway list after being formed
	def getHighway(self, coord):
		totalHighway = []
		done = False
		startCoord = Point(coord.x, coord.y)
		
		# Initial Placement
		if startCoord.x == Constants.ROWS - 1:
			totalHighway = self.goHighwayDirection(totalHighway, startCoord, Direction.UP)
		elif startCoord.x == 0:
			totalHighway = self.goHighwayDirection(totalHighway, startCoord, Direction.DOWN)
		elif startCoord.y == Constants.COLUMNS - 1:
			totalHighway = self.goHighwayDirection(totalHighway, startCoord, Direction.LEFT)
		elif startCoord.y == 0:
			totalHighway = self.goHighwayDirection(totalHighway, startCoord, Direction.RIGHT)

		# Check if done
		if len(totalHighway) >= 100 and totalHighway[len(totalHighway)-1].isBoundaryPoint():
			return totalHighway

		# Something went wrong
		totalHighway.clear()
		return totalHighway


	# Select a direction for the highway to move to
	def goHighwayDirection(self, totalHighway, point, direction):
		highwayLine = []

		# Start the initial highway placement
		highwayLine = self.setHighwayCells(totalHighway, point, direction)

		# Keep looping until a full highway is formed
		while len(highwayLine) == Constants.HIGHWAY_LENGTH:
			totalHighway.extend(highwayLine)				# Add a highway line to the total list
			point = highwayLine[len(highwayLine)-1]			# Start the next line at the last point
			probability = uniform(0, 1)						# Probability to determine the pathway

			# Continue LEFT or DOWN
			if probability < 0.19:
				if point.direction == Direction.UP or point.direction == Direction.DOWN:
					highwayLine = self.setHighwayCells(totalHighway, point, Direction.LEFT)
				elif point.direction == Direction.LEFT or point.direction == Direction.RIGHT:
					highwayLine = self.setHighwayCells(totalHighway, point, Direction.DOWN)
			# Continue RIGHT or UP
			elif probability < 0.39:
				if point.direction == Direction.UP or point.direction == Direction.DOWN:
					highwayLine = self.setHighwayCells(totalHighway, point, Direction.RIGHT)
				elif point.direction == Direction.LEFT or point.direction == Direction.RIGHT:
					highwayLine = self.setHighwayCells(totalHighway, point, Direction.UP)
			# Continue in same direction
			else:
				highwayLine = self.setHighwayCells(totalHighway, point, point.direction)

		# Loop is done, add the last highway line
		totalHighway.extend(highwayLine)
		return totalHighway


	# Set the cells to be flagged as highways
	def setHighwayCells(self, totalHighway, point, direction):
		highwayLine = []
		append = highwayLine.append
		index = 0
		done = False
		
		# If this is the first point, add it immediately
		if(len(totalHighway) == 0):
			append(point)
			index += 1

		# Loop until a full highway line is formed
		while index < Constants.HIGHWAY_LENGTH and done == False:
			# Get the next point
			newPoint = self.getNextCell(point, direction)

			# Check if the new point is within bounds, not overlapping another highway, and not already in the total list
			if(newPoint.isInBounds() and self.cells[newPoint.x, newPoint.y].isHighway == False and newPoint not in totalHighway):
				append(newPoint)
				point = highwayLine[len(highwayLine)-1]

				# If the point is a boundary point, no need to continue
				if(point.isBoundaryPoint()):
					done = True
				else:
					index += 1
			else:
				done = True

		return highwayLine


	# Get the next point depending on the direction
	def getNextCell(self, point, direction):
		if(direction == Direction.UP):
			return Point(point.x-1, point.y, Direction.UP)
		elif(direction == Direction.DOWN):
			return Point(point.x+1, point.y, Direction.DOWN)
		elif(direction == Direction.LEFT):
			return Point(point.x, point.y-1, Direction.LEFT)
		elif(direction == Direction.RIGHT):
			return Point(point.x, point.y+1, Direction.RIGHT)


	# Generate a random Point along the boundary
	def getBoundaryPoint(self):
		found = False

		while found == False:
			dimensions = [Constants.ROWS, Constants.COLUMNS]
			edges = [0 for x in range(2)]

			# Get two random points along the boundary
			edges[0] = int(randrange(0, 2) * (Constants.ROWS-1))
			edges[1] = int(randrange(0, 2) * (Constants.COLUMNS-1))

			# Change one index
			index = randrange(0, 2)
			edges[index] = randrange(0, dimensions[index])

			# Check point is not one of the four corners
			if((edges[0] != 0 and edges[1] != 0) or (edges[0] != 0 and edges[1] != 159) or (edges[0] != 119 and edges[1] != 0) or (edges[0] != 119 and edges[1] != 159)):
				found = True
			
		return Point(edges[0], edges[1])


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


	# /*\ =======================================================================
	# |*|	FOR ALGORITHMS
	# |*|		- setPaht() Sets the boolean values where the path was found
	# \*/ =======================================================================

	# Sets the boolean values at the positions inside the list
	def setPath(self, path):
		if(path != None):
			for index in range(len(path)):
				if(path[index] != self.currentStart and path[index] != self.currentGoal):
					self.cells[path[index].X, path[index].Y].isPath = True


	# Reset all the cells so algorithms can work
	def resetAlgoCells(self):
		for x in range(Constants.ROWS):
			for y in range(Constants.COLUMNS):
				self.cells[x, y].resetAlgoCell()


	# Set the start and goal
	def setNewStartGoalPair(self, index):
		self.cells[self.currentStart.X, self.currentStart.Y].isStart = False
		self.cells[self.currentGoal.X, self.currentGoal.Y].isGoal = False
		self.cells[self.startLocations[index].X, self.startLocations[index].Y].isStart = True
		self.cells[self.goalLocations[index].X, self.goalLocations[index].Y].isGoal = True
		self.currentStart = self.cells[self.startLocations[index].X, self.startLocations[index].Y]
		self.currentGoal = self.cells[self.goalLocations[index].X, self.goalLocations[index].Y]


	# /*\ =======================================================================
	# |*|	FOR LOADING & SAVING
	# |*|		- save() Saves the map with the extension .map
	# |*|		- load() Updates the cells with the info from the file
	# \*/ =======================================================================

	# Saves the grid to a .map file
	def save(self, file=None):
		# Bring up save dialog box
		if(file is None):
			file = filedialog.asksaveasfilename(filetypes=[("Map files","*.map")], defaultextension=".map", initialdir = "Resources/maps")

		# Check if user clicked cancel
		if file is None or file is '':
			return False

		# Write to file
		with open(file, 'w') as f:
			# Start and Goal locations on first two lines
			for i in range(len(self.startLocations)):
				f.write("".join(["(", str(self.startLocations[i].X), ",", str(self.startLocations[i].Y), ")"]))

			f.write('\n')

			for i in range(len(self.goalLocations)):
				f.write("".join(["(", str(self.goalLocations[i].X), ",", str(self.goalLocations[i].Y), ")"]))

			# The eight hard-to-traverse center points
			f.write('\n')
			f.write('\n'.join(str(point) for point in self.locations))
			f.write('\n')

			# The actual grid (160 characters per line)
			for row in range(Constants.ROWS):
				for col in range(Constants.COLUMNS):
					f.write(''.join(str(self.cells[row, col])))
				f.write('\n')

			f.close()

		# Show message box
		messagebox.showinfo("Map Save", "Map has been saved successfully.")
		return True


	# Saves the grid to a .map file
	def load(self, file=None):
		# Bring up save dialog box
		if(file is None):
			file = filedialog.askopenfilename(filetypes=[("Map files","*.map")], initialdir = "Resources/maps")

		# Check if user clicked cancel
		if file is None or file is '':
			return False

		# Write to file
		with open(file, 'r') as f:
			index = 0
			lines = f.read().split("\n")
			starts = [(int(x),int(y)) for x,y in re.findall(r"\((\d+),\s*(\d+)\)", lines[0])]
			goals = [(int(x),int(y)) for x,y in re.findall(r"\((\d+),\s*(\d+)\)", lines[1])]
			lines = lines[10:]
			characters = [list(line) for line in lines]

			# Set the type of cells
			for row in range(Constants.ROWS):
				for col in range(Constants.COLUMNS):
					if(characters[row][col] == '0'):
						self.cells[row, col].reset(row, col)
						self.cells[row, col].type = Type.BLOCKED
					elif(characters[row][col] == 'a'):
						self.cells[row, col].reset(row, col)
						self.cells[row, col].type = Type.REGULAR
						self.cells[row, col].isHighway = True
					elif(characters[row][col] == 'b'):
						self.cells[row, col].reset(row, col)
						self.cells[row, col].type = Type.HARD
						self.cells[row, col].isHighway = True
					elif(characters[row][col] == '1'):
						self.cells[row, col].reset(row, col)
						self.cells[row, col].type = Type.REGULAR
					elif(characters[row][col] == '2'):
						self.cells[row, col].reset(row, col)
						self.cells[row, col].type = Type.HARD

			# Get the start and goal locations
			self.startLocations.clear()
			self.goalLocations.clear()
			for row, col in starts:
				self.startLocations.append(self.cells[row, col])
			for row, col in goals:
				self.goalLocations.append(self.cells[row, col])

			self.cells[self.startLocations[0].X, self.startLocations[0].Y].isStart = True
			self.cells[self.goalLocations[0].X, self.goalLocations[0].Y].isGoal = True
			self.currentStart = self.cells[self.startLocations[0].X, self.startLocations[0].Y]
			self.currentGoal = self.cells[self.goalLocations[0].X, self.goalLocations[0].Y]
			f.close()


	# /*\ =======================================================================
	# |*|	PYGAME DRAWING
	# |*|		- draw() Calls each cell's draw function
	# \*/ =======================================================================
	def draw(self, surface, mouse):
		for x in range(Constants.ROWS):
			for y in range(Constants.COLUMNS):
				self.cells[x, y].draw(surface, mouse)
