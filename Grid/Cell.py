import math
from enum import Enum
from functools import total_ordering
import Utilities.Constants as Constants

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
	def __init__(self, x, y):
		self.isHighway = False
		self.isStart = False
		self.isGoal = False
		self.type = Type.REGULAR

		# For algorithms
		self.X = x
		self.Y = y
		self.G = math.inf
		self.Parent = None
		self.isPath = False

	# Used for tie breakers inside the heap. Checks which one is the larger G value
	def __lt__(self, other):
		return self.G > other.G

	# Equals method for use with lists (in, not in)
	def __eq__(self, other):
		return self.X == other.X and self.Y == other.Y

	# Python's toString() method
	def __str__(self):
		if self.type == Type.BLOCKED:
			return "0"
		elif self.type == Type.REGULAR and self.isHighway:
			return "a"
		elif self.type == Type.HARD and self.isHighway:
			return "b"
		elif self.type == Type.REGULAR:
			return "1"
		elif self.type == Type.HARD:
			return "2"


# Point class to hold coordinates
class Point(object):
	def __init__(self, x, y, direction = Direction.NONE):
		self.x = x
		self.y = y
		self.direction = direction

	# Check if point is a boundary coordinate
	def isBoundaryPoint(self):
		return self.x == 0 or self.x == Constants.ROWS-1 or self.y == 0 or self.y == Constants.COLUMNS-1

	# Check bounds
	def isInBounds(self):
		return self.x > -1 and self.x < Constants.ROWS and self.y > -1 and self.y < Constants.COLUMNS

	# Distance formula
	def distanceFrom(self, startPoint):
		return math.sqrt(((self.x - startPoint.x)**2) + ((self.y - startPoint.y)**2))

	# Equals method for use with lists (in, not in)
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	# Python's toString() method
	def __str__(self):
		return "".join(["(", str(self.x), ",", str(self.y), ")"])
