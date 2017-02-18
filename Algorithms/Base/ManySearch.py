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

    # For benchmarks
    self.pathlength = 0

    # Array of fringes, open and closed lists of booleans
    self.fringe = np.array([Algorithms.Base.Heap.PriorityQueue() for x in range(n)])
    self.openList = np.array([np.asmatrix([[False for y in range(Constants.COLUMNS)] for x in range(Constants.ROWS)]) for z in range(n)])


  # All Search algorithms should have their own way to find the path
  @abstractmethod
  def search(self):
    pass


  # For use with the "as" statement in the "with" clause
  def __enter__(self):
    return self


  # What to do after "with" statement is done
  def __exit__(self, *err):
    del self
