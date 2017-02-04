import math, pygame
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


# The individual Cell
class Cell(object):
	def __init__(self, x, y, rectPos=None):
		self.isHighway = False
		self.isStart = False
		self.isGoal = False
		self.type = Type.REGULAR
		self.rectPos = rectPos

		#if(self.rectPos is not None):
		#	self.rect = pygame.Rect(self.rectPos[0]+20, self.rectPos[1]+20, Constants.WIDTH+1, Constants.HEIGHT+1)

		# For algorithms
		self.X = x
		self.Y = y
		self.G = math.inf
		self.Parent = None
		self.isPath = False

	# Reset the cell
	def reset(self, x, y):
		self.isHighway = False
		self.isStart = False
		self.isGoal = False
		self.Type = Type.REGULAR
		self.X = x
		self.Y = y
		self.G = math.inf
		self.Parent = None
		self.isPath = False

	# Reset the algorithm values
	def resetAlgoCell(self):
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

	# Draw for pygame
	def draw(self, surface, mouse):
		color = Constants.GREEN

		if self.type == Type.HARD: 		
			color = Constants.GREY				# Hard to traverse
		if self.type == Type.BLOCKED:
			color = Constants.BLACK				# Blocked path
		if self.isHighway and self.type == Type.HARD:
			color = Constants.DARK_BLUE			# Highway and hard to traverse
		if self.isHighway and self.type == Type.REGULAR:
			color = Constants.LIGHT_BLUE		# Highway and regular
		if self.isStart == True:			
			color = Constants.WHITE				# Start vertex
		if self.isGoal == True:			
			color = Constants.RED				# Goal vertex

		if self.isPath == True:					# Part of path
			color = Constants.YELLOW
			if self.type == Type.HARD:
				color = Constants.DARK_YELLOW


		# For mouse hover (not accurate)
		# if(self.rect.collidepoint(mouse)):
		#	pygame.draw.rect(surface, Constants.RED, self.rectPos, 1)

		# Draw the cell
		pygame.draw.rect(surface, color, self.rectPos)
