import math
import Utilities.Constants as Constants
from Grid.Cell import Type

# /*\ =======================================================================
# |*|	HEURISTICS
# |*|		- Default for AStar
# |*|		- Manhattan Distance
# |*|		- Euclidean Distance
# |*|		- Euclidean Distance Sqaured
# \*/ =======================================================================
def NoHeuristic(s, goal, grid):
	return 0

def AStarHeuristic(s, goal, grid):
	a = math.sqrt(2)
	min_XY = min(abs(s.X - goal.X), abs(s.Y - goal.Y))
	max_XY = max(abs(s.X - goal.X), abs(s.Y - goal.Y))

	return (a * min_XY) + max_XY - min_XY

# Optimized for the vertical and horizontal path
def ManhattanDistance(s, goal, grid):
	dx = abs(s.X - goal.X)
	dy = abs(s.Y - goal.Y)
	cost = math.inf

	for sprime in Successors(s, grid):
		temp = PathCost(s, sprime)
		if(temp < cost):
			cost = temp

	return cost * (dx + dy)

# Straight line distance
def EuclideanDistance(s, goal, grid):
	dx = abs(s.X - goal.X)
	dy = abs(s.Y - goal.Y)
	cost = math.inf

	for sprime in Successors(s, grid):
		temp = PathCost(s, sprime)
		if(temp < cost):
			cost = temp

	return cost * math.sqrt(dx*dx + dy*dy)

# Loses the triangle equality (ex: Distance from (0,0) to (2,0) is 4)
def EuclideanDistanceSquared(s, goal, grid):
	dx = abs(s.X - goal.X)
	dy = abs(s.Y - goal.Y)
	cost = math.inf

	for sprime in Successors(s, grid):
		temp = PathCost(s, sprime)
		if(temp < cost):
			cost = temp

	return cost * (dx*dx + dy*dy)


# /*\ =======================================================================
# |*|	OTHER FORMULAS
# |*|		- Successors (returns up to 8 cells around 's')
# |*|		- PathCost (gets the cost from traversing from 's' to 'sprime')
# \*/ =======================================================================

# Get the neighboring cells around 's'
def Successors(s, grid):
	cells = []
	append = cells.append

	# Start from the top left of the 's' cell and get all cells that are not blocked
	for row in range(s.X-1, s.X+2):
		for col in range(s.Y-1, s.Y+2):
			# If row and column are on 's' or if the row and column are out of bounds, skip
			if(row == s.X and col == s.Y):
				continue
			if(row < 0 or row > Constants.ROWS-1 or col < 0 or col > Constants.COLUMNS-1):
				continue

			if(grid[row, col].type != Type.BLOCKED):
				append(grid[row, col])

	return cells


# Get the cost from traversing from one cell to a neighboring cell
def PathCost(s, sprime):
	cost = 0
	sType = s.type
	sprimeType = sprime.type

	# DIAGONAL
	if(s.X != sprime.X and s.Y != sprime.Y):
		if(sType == Type.REGULAR and sprimeType == Type.REGULAR):
			cost = math.sqrt(2)
		elif(sType == Type.HARD and sprimeType == Type.HARD):
			cost = math.sqrt(8)
		elif((sType == Type.REGULAR and sprimeType == Type.HARD) or (sType == Type.HARD and sprimeType == Type.REGULAR)):
			cost = (math.sqrt(2) + math.sqrt(8)) / 2

	# HORIZONTAL/VERTICAL
	else:
		if(sType == Type.REGULAR and sprimeType == Type.REGULAR):
			cost = 0.25 if s.isHighway and sprime.isHighway else 1
		elif(sType == Type.HARD and sprimeType == Type.HARD):
			cost = 0.50 if s.isHighway and sprime.isHighway else 2
		elif((sType == Type.REGULAR and sprimeType == Type.HARD) or (sType == Type.HARD and sprimeType == Type.REGULAR)):
			cost = 0.375 if s.isHighway and sprime.isHighway else 1.5

	return cost
