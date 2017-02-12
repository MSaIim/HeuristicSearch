import numpy as np
import Algorithms.Base.Heap
import Utilities.Constants as Constants
from abc import ABC, abstractmethod

# Abstract class ManySearch
class ManySearch(ABC):
  def __init__(self, grid, start, goal, n, w1, w2, heuristics):
    self.grid = grid
    self.start = start
    self.goal = goal
    self.n = n
    self.w1 = w1
    self.w2 = w2
    self.heuristics = heuristics
    self.time = 0
    self.endIndex = 0

    # For benchmarks
    self.pathlength = 0
    self.nodeexpanded = np.array([0 for x in range(n)])

    # Array of grids
    self.cells = np.array([self.grid for x in range(n)])

    # Array to keep track of sprimes
    self.tracker = np.array([np.asmatrix([[False for y in range(Constants.COLUMNS)] for x in range(Constants.ROWS)]) for z in range(n)])

    # Array of fringes, open and closed lists of booleans
    self.fringe = np.array([Algorithms.Base.Heap.PriorityQueue() for x in range(n)])
    self.openList = np.array([np.asmatrix([[False for y in range(Constants.COLUMNS)] for x in range(Constants.ROWS)]) for z in range(n)])
    self.closedList = np.array([np.asmatrix([[False for y in range(Constants.COLUMNS)] for x in range(Constants.ROWS)]) for z in range(n)])


  # All Search algorithms should have their own way to find the path
  @abstractmethod
  def search(self):
    pass


  # Get the key for priority
  def Key(self, s, i):
    self.cells[i][s.X, s.Y].H = self.heuristics[i](s, self.goal)
    self.cells[i][s.X, s.Y].F = self.cells[i][s.X, s.Y].G + self.cells[i][s.X, s.Y].H
    return self.cells[i][s.X, s.Y].G + self.w1 * self.cells[i][s.X, s.Y].H
    

  # Get the path from the start to the goal
  def getPath(self):
    searchPath = []
    append = searchPath.append
    done = False
    cell = self.cells[self.endIndex][self.goal.X, self.goal.Y]

    while done == False:
      append(cell)

      if(cell == self.start):
        done = True

      cell = cell.Parent

    # For benchmarks
    self.pathlength = self.cells[self.endIndex][self.goal.X, self.goal.Y].G

    return searchPath


  # For use with the "as" statement in the "with" clause
  def __enter__(self):
    return self


  # What to do after "with" statement is done
  def __exit__(self, *err):
    del self
