from random import randrange, uniform
from Cell import Type
from Cell import Cell
from Cell import Point

class Grid(object):
	def __init__(self):
		self.initialize()

	def initialize(self):
		# Create 2D array of Cells (120 rows by 160 columns)
		self.cells = [[Cell() for x in range(160)] for x in range(120)]

		# Array to hold 8 random coordinates
		locations = [Point(0, 0) for x in range(8)]
		index = 0

		# Select 8 distinct random coordinates
		while(index < 8):
			temp = Point(randrange(0, 119), randrange(0, 159))
			if(temp not in locations):
				locations[index] = temp
				print(index+1, "-", locations[index].x, ",", locations[index].y)
				index += 1

		# 50% probability to make a cell HARD TO TRAVERSE around the coordinates chosen above
		for location in locations:
			for row in range(location.x - 15, location.x + 15):
				for col in range(location.y - 15, location.y + 15):
					if(row > -1 and row < 120 and col > -1 and col < 160):
						if(uniform(0, 1) > 0.49):
							self.cells[row][col].type = Type.HARD

		# Create a highway
		