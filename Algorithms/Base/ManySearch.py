import numpy as np
import Algorithms.Base.Heap
import Utilities.Constants as Constants
from abc import ABC, abstractmethod

# Abstract class ManySearch
class ManySearch(ABC):
  def __init__(self, grid, n, w1, w2, heuristics, i):
    # Reset the grid
    grid.resetAlgoCells()

    # Initial setup
    self.grid = grid.cells
    self.n = n
    self.w1 = w1
    self.w2 = w2
    self.heuristics = heuristics
    self.time = 0
    self.start = grid.currentStart if i == -1 else grid.startLocations[i]
    self.goal = grid.currentGoal if i == -1 else grid.goalLocations[i]

    # Path list
    self.searchPath = []

    # For benchmarks
    self.pathlength = 0
    self.nodeexpanded = 0

    # Array of fringes, open and closed lists of booleans
    self.fringe = np.array([Algorithms.Base.Heap.PriorityQueue() for x in range(n)])
    self.openList = np.array([np.asmatrix([[False for y in range(Constants.COLUMNS)] for x in range(Constants.ROWS)]) for z in range(n)])


  # All Search algorithms should have their own way to find the path
  @abstractmethod
  def search(self):
    pass


  # Get the path from start to the goal
  def getPath(self):
    return self.searchPath


  # Trace the path from the start to the goal
  def tracePath(self, cellData):
    append = self.searchPath.append
    cell = cellData[self.goal.X, self.goal.Y]

    # Trace path back to start
    while cell is not self.start:
      append(cell)
      cell = cellData[cell.X, cell.Y].Parent

    # Assign f, g, h values
    for row in range(Constants.ROWS):
      for col in range(Constants.COLUMNS):
        self.grid[row, col].F = cellData[row, col].F
        self.grid[row, col].G = cellData[row, col].G
        self.grid[row, col].H = cellData[row, col].H

    # Set start g value
    self.grid[self.start.X, self.start.Y].G = 0

    # For benchmarks
    self.pathlength = cellData[self.goal.X, self.goal.Y].G


  # For use with the "as" statement in the "with" clause
  def __enter__(self):
    return self


  # What to do after "with" statement is done
  def __exit__(self, *err):
    del self
