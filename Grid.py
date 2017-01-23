from random import randrange, uniform
from Cell import Type
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
		rows = self.ROWS-1
		columns = self.COLUMNS-1
		hLength = 20

		# GO DOWN
		if coord.x == 0:
			for index in range(hLength):
				if self.cells[index][coord.y].isHighway == False:
					points.append(Point(index, coord.y))
		# GO UP
		elif coord.x == rows:
			for index in reversed(range(rows-hLength+1, self.ROWS)):
				if self.cells[index][coord.y].isHighway == False:
					points.append(Point(index, coord.y))
		# GO RIGHT
		elif coord.y == 0:
			for index in range(hLength):
				if self.cells[coord.x][index].isHighway == False:
					points.append(Point(coord.x, index))
		# GO LEFT
		elif coord.y == columns:
			for index in reversed(range(columns-hLength+1, self.COLUMNS)):
				if self.cells[coord.x][index].isHighway == False:
					points.append(Point(coord.x, index))

		# Check size of highway
		if len(points) == 20:
			for point in points:
				self.cells[point.x][point.y].isHighway = True
			return True

		# Something went wrong
		return False
