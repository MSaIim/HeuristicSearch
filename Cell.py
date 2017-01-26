from enum import Enum

# Enumeration class to know the Cell's type
class Type(Enum):
	REGULAR = 1
	HARD = 2
	BLOCKED = 3

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

	def __eq__(self, other):
		return int(self.x) == int(other.x) and int(self.y) == int(other.y)