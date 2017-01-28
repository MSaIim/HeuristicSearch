import math
from enum import Enum

# Enum class to know the Cell's type
class Type(Enum):
	REGULAR = 1
	HARD = 2
	BLOCKED = 3

# Enum class to know direction of the points
class Direction(Enum):
	NONE = 1
	UP = 2
	DOWN = 3
	LEFT = 4
	RIGHT = 5


# The individual Cell
class Cell(object):
	def __init__(self):
		self.isHighway = False
		self.isStart = False
		self.isGoal = False
		self.type = Type.REGULAR


# Point class to hold coordinates
class Point(object):
	def __init__(self, x, y, direction = Direction.NONE):
		self.x = int(x)
		self.y = int(y)
		self.direction = direction

	# Check if point is a boundary coordinate
	def isBoundaryPoint(self):
		return self.x == 0 or self.x == 119 or self.y == 0 or self.y == 159

	# Check bounds
	def isInBounds(self):
		return self.x > -1 and self.x < 120 and self.y > -1 and self.y < 160

	# Distance formula
	@staticmethod
	def calcDistance(pointOne, pointTwo):
		return math.sqrt(((pointOne.x - pointTwo.x)**2) + ((pointOne.y - pointTwo.x)**2))

	# Equals method for use with lists (in, not in)
	def __eq__(self, other):
		return int(self.x) == int(other.x) and int(self.y) == int(other.y)
