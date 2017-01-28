from copy import deepcopy
from random import randrange, uniform
from py import Constants
from py.Cell import Cell, Direction, Point

class Highway(object):
	def createHighway(self, gridCells):
		self.cells = gridCells

		# Loop until a good highway is formed
		done = False
		while done == False:
			coord = self.getBoundaryPoint()			# Get a random border point
			highway = self.getHighway(coord)		# Get a list of points
			if(len(highway) >= 100):				# Check if highway is good
				done = True
				print("\t", coord.x, coord.y)

		# Return good highway
		return highway


	# Get the highway list after being formed
	def getHighway(self, coord):
		totalHighway = []
		done = False
		startCoord = deepcopy(coord)
		
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
	def goHighwayDirection(self, totalHighway, coord, direction):
		highwayLine = []
		point = deepcopy(coord)

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
	def setHighwayCells(self, totalHighway, coord, direction):
		highwayLine = []
		index = 0
		done = False
		point = deepcopy(coord)
		
		# If this is the first point, add it immediately
		if(len(totalHighway) == 0):
			highwayLine.append(point)
			index += 1

		# Loop until a full highway line is formed
		while index < Constants.HIGHWAY_LENGTH and done == False:
			# Get the next point
			newPoint = self.getNextCell(point, direction)

			# Check if the new point is within bounds, not overlapping another highway, and not already in the total list
			if(newPoint.isInBounds() and self.cells[newPoint.x][newPoint.y].isHighway == False and newPoint not in totalHighway):
				highwayLine.append(newPoint)
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