from random import randrange, uniform
from Cell import Type
from Cell import Direction
from Cell import Cell
from Cell import Point

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


	# Create highway by going 20 cells in a direction
	def createHighway(self, coord):
		points = []
		done = False
		
		# Initial Placement
		if coord.x == self.ROWS - 1:
			points = self.setHighwayCells(coord, Direction.UP)
			coord.direction = Direction.UP
		elif coord.x == 0:
			points = self.setHighwayCells(coord, Direction.DOWN)
			coord.direction = Direction.DOWN
		elif coord.y == self.COLUMNS - 1:
			points = self.setHighwayCells(coord, Direction.LEFT)
			coord.direction = Direction.LEFT
		elif coord.y == 0:
			points = self.setHighwayCells(coord, Direction.RIGHT)
			coord.direction = Direction.RIGHT

		#done = True
		if len(points) == 20:
			# Cotinue highway
			points = self.setHighwayDirection(coord, points)
			if len(points) >= 100 and self.isBoundaryPoint(points[-1]):
				done = True

			# Highway complete
			if done == True:
				for point in points:
					self.cells[point.x][point.y].isHighway = True
				return True

		# Something went wrong
		return False


	# Select a direction for the highway to move to
	def setHighwayDirection(self, coord, points):
		highwayLeg = []
		tries = 0

		while tries < 4:
			probability = uniform(0, 1)

			# Continue in same direction
			if probability < 0.59:
				if coord.direction == Direction.UP:
					highwayLeg = self.setHighwayCells(coord, Direction.UP)
				elif coord.direction == Direction.DOWN:
					highwayLeg = self.setHighwayCells(coord, Direction.DOWN)
				elif coord.direction == Direction.LEFT:
					highwayLeg = self.setHighwayCells(coord, Direction.LEFT)
				elif coord.direction == Direction.RIGHT:
					highwayLeg = self.setHighwayCells(coord, Direction.RIGHT)
			# Continue in perpendicular (DOWN or LEFT)
			elif probability < 0.79:
				if coord.direction == Direction.UP or coord.direction == Direction.DOWN:
					highwayLeg = self.setHighwayCells(coord, Direction.LEFT)
				elif coord.direction == Direction.LEFT or coord.direction == Direction.RIGHT:
					highwayLeg = self.setHighwayCells(coord, Direction.DOWN)
			# Continue in perpendicular (UP or RIGHT)
			elif probability < 1:
				if coord.direction == Direction.UP or coord.direction == Direction.DOWN:
					highwayLeg = self.setHighwayCells(coord, Direction.RIGHT)
				elif coord.direction == Direction.LEFT or coord.direction == Direction.RIGHT:
					highwayLeg = self.setHighwayCells(coord, Direction.UP)

			if len(points) + len(highwayLeg) >= 100 and self.isBoundaryPoint(highwayLeg[-1]):
				points.extend(highwayLeg)
				break;
			elif len(highwayLeg) < 20 or self.isBoundaryPoint(highwayLeg[-1]):
				tries += 1
			else:
				coord = highwayLeg[len(highwayLeg)-1]
				points.extend(highwayLeg)
		
		return points


	# Set the cells to be flagged as highways
	def setHighwayCells(self, cell, direction):
		highwayLength = 20
		highway = []
		index = 0

		while index < 20:
			point = self.getNextCell(cell, direction)
			if(self.isInBounds(point) and self.cells[point.x][point.y].isHighway == False):
				highway.append(point)
				cell = highway[-1]
				index += 1
			else:
				break

		return highway


	def getNextCell(self, cell, direction):
		if(direction == Direction.UP):
			return Point(cell.x-1, cell.y, Direction.UP)
		elif(direction == Direction.DOWN):
			return Point(cell.x+1, cell.y, Direction.DOWN)
		elif(direction == Direction.LEFT):
			return Point(cell.x, cell.y-1, Direction.LEFT)
		elif(direction == Direction.RIGHT):
			return Point(cell.x, cell.y+1, Direction.RIGHT)


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


	# Check if point is a boundary coordinate
	def isBoundaryPoint(self, point):
		return point.x == 0 or point.x == 119 or point.y == 0 or point.y == 159


	# Check bounds
	def isInBounds(self, point):
		return point.x > -1 and point.x < 120 and point.y > -1 and point.y < 160

