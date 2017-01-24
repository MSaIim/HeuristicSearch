from random import randrange, uniform
from Cell import Type
from Cell import Direction
from Cell import Cell
from Cell import Point

class Grid(object):
	ROWS = 120
	COLUMNS = 160
	NUMPOINTS = 8
	NUMHIGHWAYS = 1
	highwayTurns = []

	def __init__(self):
		self.initialize()
		print("")


	def initialize(self):
		# Create 2D array of Cells (120 rows by 160 columns)
		self.cells = [[Cell() for x in range(self.COLUMNS)] for x in range(self.ROWS)]

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
		for index in range(self.NUMHIGHWAYS):
			edges = [Point(0,0) for x in range(self.NUMHIGHWAYS)]
			
			while(True):
				coord = self.getBoundaryPoint()
				if(self.createHighway(coord) == True):
					break

			print("\t", coord.x, coord.y)


	# Generate a random Point along the boundary
	def getBoundaryPoint(self):
		dimensions = [self.ROWS, self.COLUMNS]
		edges = [0 for x in range(2)]

		# Get two random points along the boundary
		edges[0] = randrange(0, 2) * (self.ROWS-1)
		edges[1] = randrange(0, 2) * (self.COLUMNS-1)

		# Change one index
		index = randrange(0, 2)
		edges[index] = randrange(0, dimensions[index])

		# Return random Point
		return Point(edges[0], edges[1])


	# Create highway by going 20 cells in a direction
	def createHighway(self, coord):
		points = []
		done = False
		probability = uniform(0, 1)

		# Initial Placement
		if coord.x == self.ROWS - 1:
			points = self.setHighwayCells(coord, points, Direction.UP)
		elif coord.x == 0:
			points = self.setHighwayCells(coord, points, Direction.DOWN)
		elif coord.y == self.COLUMNS - 1:
			points = self.setHighwayCells(coord, points, Direction.LEFT)
		elif coord.y == 0:
			points = self.setHighwayCells(coord, points, Direction.RIGHT)

		# Continue Highway
		if len(points) == 20:
			while(True):
				# Check if all options exhausted
				if len(self.highwayTurns) == 3:
					del points[:]
					del self.highwayTurns[:]
					break

				# Get last index and coordinate
				index = len(points) - 1
				coord = points[index]

				# Continue the highway
				points = self.setHighwayDirection(coord, points, probability)

				# Check if highway is done
				if len(points) >= 100 and self.isBoundaryPoint(points[len(points) - 1]) == True:
		 			done = True
		 			break
		 		# Something went wrong, delete the points that were just added
				elif len(points) % 20 != 0:
					del points[index:]
					self.highwayTurns.append(probability)	# Add the probability to try a different path

		# Highway complete
		if done == True:
			for point in points:
				self.cells[point.x][point.y].isHighway = True
			return True

		# Something went wrong
		return False


	# Select a direction for the highway to move to
	def setHighwayDirection(self, coord, points, probability):
		# Check if a direction failed. Go a different route
		if(len(self.highwayTurns) > 0):
			if self.highwayTurns[len(self.highwayTurns)-1] < 0.59:
				probability = 0.70	# Try going DOWN or LEFT
			elif self.highwayTurns[len(self.highwayTurns)-1] > 0.59 and self.highwayTurns[len(self.highwayTurns)-1] < 0.79:
				probability = 0.90	# Try going UP or RIGHT
			else:
				probability = 0.50	# Try going in the same direction

		# Continue in same direction
		if probability < 0.59:
			if coord.direction == Direction.UP:
				points = self.setHighwayCells(coord, points, Direction.UP)
			elif coord.direction == Direction.DOWN:
				points = self.setHighwayCells(coord, points, Direction.DOWN)
			elif coord.direction == Direction.LEFT:
				points = self.setHighwayCells(coord, points, Direction.LEFT)
			elif coord.direction == Direction.RIGHT:
				points = self.setHighwayCells(coord, points, Direction.RIGHT)

		# Continue in perpendicular (DOWN or LEFT)
		elif probability < 0.79:
			if coord.direction == Direction.UP or coord.direction == Direction.DOWN:
				points = self.setHighwayCells(coord, points, Direction.LEFT)
			elif coord.direction == Direction.LEFT or coord.direction == Direction.RIGHT:
				points = self.setHighwayCells(coord, points, Direction.DOWN)

		# Continue in perpendicular (UP or RIGHT)
		elif probability < 1:
			if coord.direction == Direction.UP or coord.direction == Direction.DOWN:
				points = self.setHighwayCells(coord, points, Direction.RIGHT)
			elif coord.direction == Direction.LEFT or coord.direction == Direction.RIGHT:
				points = self.setHighwayCells(coord, points, Direction.UP)

		return points


	# Set the cells to be flagged as highways
	def setHighwayCells(self, cell, points, direction):
		highwayLength = 20

		# GO UP
		if direction == Direction.UP:
			for index in range(cell.x-highwayLength, cell.x+1):
				if(index > 0 and self.cells[index][cell.y].isHighway == False):
					points.append(Point(index, cell.y, Direction.UP))

		# GO DOWN
		elif direction == Direction.DOWN:
			for index in range(cell.x, cell.x+highwayLength):
				if(index < self.ROWS and self.cells[index][cell.y].isHighway == False):
					points.append(Point(index, cell.y, Direction.DOWN))

		# GO LEFT
		elif direction == Direction.LEFT:
			for index in range(cell.y-highwayLength, cell.y+1):
				if(index >= 0 and self.cells[cell.x][index].isHighway == False):
					points.append(Point(cell.x, index, Direction.LEFT))

		# GO RIGHT
		elif direction == Direction.RIGHT:
			for index in range(cell.y, cell.y+highwayLength):
				if(index < self.COLUMNS and self.cells[cell.x][index].isHighway == False):
					points.append(Point(cell.x, index, Direction.RIGHT))

		return points


	# Check if point is a boundary coordinate
	def isBoundaryPoint(self, point):
		return point.x == 0 or point.x == 119 or point.y == 0 or point.y == 159