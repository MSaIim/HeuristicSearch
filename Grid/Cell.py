import math, pygame
from enum import Enum
from functools import total_ordering
import Utilities.Constants as Constants

# /*\ =======================================================================
# |*| TYPE ENUM CLASS
# |*|   - Holds the types for an individual cell
# \*/ =======================================================================
class Type(Enum):
  REGULAR = 1
  HARD = 2
  BLOCKED = 3


# /*\ =======================================================================
# |*| DIRECTION ENUM CLASS
# |*|   - Used to build highways
# \*/ =======================================================================
class Direction(Enum):
  NONE = 1
  UP = 2
  DOWN = 3
  LEFT = 4
  RIGHT = 5


# /*\ =======================================================================
# |*| POINT CLASS
# |*|   - Used to build the grid
# |*|   - Has helper functions to know a cell's location
# \*/ =======================================================================
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


# /*\ =======================================================================
# |*| CELL CLASS
# |*|   - Holds the details of a cell
# |*|   - Holds the information that the algorithms use
# |*|   - Used to color a cell through pygame's draw call
# \*/ =======================================================================
class Cell(object):
  def __init__(self, x, y, rectPos=None):
    self.isHighway = False
    self.isStart = False
    self.isGoal = False
    self.type = Type.REGULAR
    self.rectPos = rectPos

    # For algorithms
    self.X = x
    self.Y = y
    self.F = 0
    self.G = 0
    self.H = 0
    self.Priority = 0
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
    self.resetAlgoCell()

  # Reset the algorithm values
  def resetAlgoCell(self):
    self.F = 0
    self.G = 0
    self.H = 0
    self.Priority = 0
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
      color = Constants.GREY          # Hard to traverse
    if self.type == Type.BLOCKED:
      color = Constants.BLACK         # Blocked path
    if self.isHighway and self.type == Type.HARD:
      color = Constants.DARK_BLUE     # Highway and hard to traverse
    if self.isHighway and self.type == Type.REGULAR:
      color = Constants.HIGHWAY_BLUE  # Highway and regular
    if self.isStart == True:      
      color = Constants.START_COLOR   # Start vertex
    if self.isGoal == True:     
      color = Constants.RED           # Goal vertex

    if self.isPath == True:           # Part of path
      color = Constants.YELLOW
      if self.type == Type.HARD:
        color = Constants.DARK_YELLOW


    # Draw the cell
    pygame.draw.rect(surface, color, self.rectPos)
