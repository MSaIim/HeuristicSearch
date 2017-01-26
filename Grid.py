import math
from random import randrange, uniform
from Cell import Type
from Cell import Direction
from Cell import Cell
from Cell import Point
from copy import deepcopy

class Grid(object):
	ROWS = 120
	COLUMNS = 160
	NUMPOINTS = 8
	NUMHIGHWAYS = 4

	def __init__(self):
		self.initialize()
		print("")


	def initialize(self):
		# Create 2D array of Cells (120 rows by 160 columns)
		self.cells = [[Cell() for x in range(self.COLUMNS)] for x in range(self.ROWS)]

		# start and goal locations
		self.startLocation = Point(0,0)
		self.goalLocation = Point(0,0)

		# Array to hold 8 random coordinates
		locations = [Point(0, 0) for x in range(self.NUMPOINTS)]
		index = 0

		# Select 8 distinct random coordinates
		print("Center Points:")
		while(index < self.NUMPOINTS):
			temp = Point(randrange(0, self.ROWS-1), randrange(0, self.COLUMNS-1))
			if(temp not in locations):
				locations[index] = temp
				index += 1
				print("\t", locations[index-1].x, locations[index-1].y)

		# 50% probability to make a cell HARD TO TRAVERSE around the coordinates chosen above
		for location in locations:
			for row in range(location.x - 15, location.x + 15):
				for col in range(location.y - 15, location.y + 15):
					if(row > -1 and row < self.ROWS and col > -1 and col < self.COLUMNS):
						if(uniform(0, 1) > 0.49):
							self.cells[row][col].type = Type.HARD

		# Create a highway
		print("\nHighway Points:")
		
		i = 0	
		while(i < self.NUMHIGHWAYS):
			coord = self.getBoundaryPoint()
			if(self.createHighway(coord) == True):
				i += 1
				print("\t", coord.x, coord.y)

		# Choose blocked cells
		blockedCells = 0
		while(blockedCells < (self.ROWS * self.COLUMNS) * 0.2):
			x = randrange(0, 120)
			y = randrange(0, 160)

			if(self.cells[x][y].isHighway == False):
				self.cells[x][y].type = Type.BLOCKED
				blockedCells += 1

		# Choose start vertex
		found = False
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

			if(self.cells[point.x][point.y].type != Type.BLOCKED and self.calcDistance(point) > 100):
				self.cells[point.x][point.y].isGoal = True
				self.goalLocation = point
				found = True


	# Create highway by going 20 cells in a direction
	def createHighway(self, cell):
		totalHighway = []
		done = False
		startCoord = deepcopy(cell)
		
		# Initial Placement
		if startCoord.x == self.ROWS - 1:
			totalHighway = self.goHighwayDirection(totalHighway, startCoord, Direction.UP)
		elif startCoord.x == 0:
			totalHighway = self.goHighwayDirection(totalHighway, startCoord, Direction.DOWN)
		elif startCoord.y == self.COLUMNS - 1:
			totalHighway = self.goHighwayDirection(totalHighway, startCoord, Direction.LEFT)
		elif startCoord.y == 0:
			totalHighway = self.goHighwayDirection(totalHighway, startCoord, Direction.RIGHT)

		# Check if done
		if len(totalHighway) >= 100 and self.isBoundaryPoint(totalHighway[len(totalHighway)-1]):
			done = True

		# Highway complete
		if done == True:
			for point in totalHighway:
				self.cells[point.x][point.y].isHighway = True
			return True

		# Something went wrong
		return False


	# Select a direction for the highway to move to
	def goHighwayDirection(self, totalHighway, coord, direction):
		highwayLine = []
		tries = 0
		done = False
		point = deepcopy(coord)

		highwayLine = self.setHighwayCells(totalHighway, point, direction)
		while len(highwayLine) == 20:
			totalHighway.extend(highwayLine)
			point = highwayLine[len(highwayLine)-1]
			probability = uniform(0, 1)

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

		totalHighway.extend(highwayLine)
		return totalHighway


	# Set the cells to be flagged as highways
	def setHighwayCells(self, totalHighway, coord, direction):
		highwayLength = 20
		highwayLine = []
		index = 0
		done = False
		point = deepcopy(coord)
		
		if(len(totalHighway) == 0):
			highwayLine.append(point)
			index += 1

		while index < 20 and done == False:
			newPoint = self.getNextCell(point, direction)

			if(self.isInBounds(newPoint) and self.cells[newPoint.x][newPoint.y].isHighway == False and newPoint not in totalHighway):
				highwayLine.append(newPoint)
				point = highwayLine[len(highwayLine)-1]

				if(self.isBoundaryPoint(point) == True):
					done = True
				else:
					index += 1
			else:
				done = True

		return highwayLine


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
			dimensions = [self.ROWS, self.COLUMNS]
			edges = [0 for x in range(2)]

			# Get two random points along the boundary
			edges[0] = int(randrange(0, 2) * (self.ROWS-1))
			edges[1] = int(randrange(0, 2) * (self.COLUMNS-1))

			# Change one index
			index = randrange(0, 2)
			edges[index] = randrange(0, dimensions[index])

			if((edges[0] != 0 and edges[1] != 0) or (edges[0] != 0 and edges[1] != 159) or (edges[0] != 119 and edges[1] != 0) or (edges[0] != 119 and edges[1] != 159)):
				found = True
				return Point(edges[0], edges[1])


	# Check if point is a boundary coordinate
	def isBoundaryPoint(self, point):
		return point.x == 0 or point.x == 119 or point.y == 0 or point.y == 159


	# Check bounds
	def isInBounds(self, point):
		return point.x > -1 and point.x < 120 and point.y > -1 and point.y < 160

	# Distance formula
	def calcDistance(self, point):
		return math.sqrt(((point.x - self.startLocation.x)**2) + ((point.y - self.startLocation.x)**2))

	# Get border points
	def getBorderCells(self):
		borderCells = []

		for i in range(0, 20):
			for j in range(0, 160):
				borderCells.append(Point(i, j))

		for i in range(99, 120):
			for j in range(0, 160):
				borderCells.append(Point(i, j))

		for i in range(0, 20):
			for j in range(0, 120):
				borderCells.append(Point(j, i))

		for i in range(139, 160):
			for j in range(0, 120):
				borderCells.append(Point(j, i))

		return borderCells;