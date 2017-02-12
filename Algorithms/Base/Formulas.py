import math
import Utilities.Constants as Constants
from Grid.Cell import Type

# /*\ =======================================================================
# |*|	HEURISTICS
# |*|		- Default for AStar
# |*|		- Manhattan Distance
# |*|		- Euclidean Distance
# |*|		- Chebyshev Distance
# |*|		- Diagonal Distance
# \*/ =======================================================================
def NoHeuristic(s, goal):
	return 0

def AStarHeuristic(s, goal):
	a = math.sqrt(2)
	min_XY = min(abs(s.X - goal.X), abs(s.Y - goal.Y))
	max_XY = max(abs(s.X - goal.X), abs(s.Y - goal.Y))

	return (a * min_XY) + max_XY - min_XY

# Optimized for the vertical and horizontal path
def ManhattanDistance(s, goal):
	dx = abs(s.X - goal.X)
	dy = abs(s.Y - goal.Y)

	return 0.25 * (dx + dy)

# Straight line distance
def EuclideanDistance(s, goal):
	dx = s.X - goal.X
	dy = s.Y - goal.Y

	return 0.25 * math.sqrt(dx*dx + dy*dy)

# Max of values
def ChebyshevDistance(s, goal):
	dx = abs(s.X - goal.X)
	dy = abs(s.Y - goal.Y)

	return max(dx, dy)

# PRefer diagonal
def DiagonalDistance(s, goal):
	d_max = max(abs(s.X - goal.X), abs(s.Y - goal.Y))
	d_min = min(abs(s.Y - goal.Y), abs(s.Y - goal.Y))

	horizontal_min = 0.25
	diagonal_min = 1.41421356237
	
	return diagonal_min * d_min + horizontal_min * (d_max - d_min)


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
			cost = 1.41421356237	# sqrt(2)
		elif(sType == Type.HARD and sprimeType == Type.HARD):
			cost = 2.82842712475	# sqrt(8)
		elif((sType == Type.REGULAR and sprimeType == Type.HARD) or (sType == Type.HARD and sprimeType == Type.REGULAR)):
			cost = 2.12132034356	# (sqrt(2) + sqrt(8)) / 2

	# HORIZONTAL/VERTICAL
	else:
		if(sType == Type.REGULAR and sprimeType == Type.REGULAR):
			cost = 0.25 if s.isHighway and sprime.isHighway else 1
		elif(sType == Type.HARD and sprimeType == Type.HARD):
			cost = 0.50 if s.isHighway and sprime.isHighway else 2
		elif((sType == Type.REGULAR and sprimeType == Type.HARD) or (sType == Type.HARD and sprimeType == Type.REGULAR)):
			cost = 0.375 if s.isHighway and sprime.isHighway else 1.5

	return cost
