import numpy as np
import Algorithms.Base.Heap
import Utilities.Constants as Constants
from abc import ABC, abstractmethod

# Abstract class Search
class SingleSearch(ABC):
  def __init__(self, grid, heuristic, i):
    # Reset the grid
    grid.resetAlgoCells()

    # Initial setup
    self.grid = grid.cells
    self.Heuristic = heuristic
    self.time = 0
    self.start = grid.currentStart if i == -1 else grid.startLocations[i]
    self.goal = grid.currentGoal if i == -1 else grid.goalLocations[i]

    # For benchmarks
    self.pathlength = 0
    self.nodeexpanded = 0

    # Min Heap to hold nodes that might be expanded
    self.fringe = Algorithms.Base.Heap.PriorityQueue()

    # 2D array of booleans to know which cell is in the fringe
    self.openList = np.asmatrix([[False for y in range(Constants.COLUMNS)] for x in range(Constants.ROWS)])
    self.closedList = np.asmatrix([[False for y in range(Constants.COLUMNS)] for x in range(Constants.ROWS)])


  # All Search algorithms should have their own way to find the path
  @abstractmethod
  def search(self):
    pass


  # Get the path from the start to the goal
  def getPath(self):
    searchPath = []
    done = False
    cell = self.goal

    while done == False:
      searchPath.append(cell)

      if(cell == self.start):
        done = True

      cell = cell.Parent

    return searchPath


  # For use with the "as" statement in the "with" clause
  def __enter__(self):
    return self


  # What to do after "with" statement is done
  def __exit__(self, *err):
    del self
