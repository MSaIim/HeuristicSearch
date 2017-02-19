import math, time
import numpy as np
from Grid.Cell import AlgoCell
import Utilities.Constants as Constants
import Algorithms.Base.Formulas as Formulas
from Algorithms.Base.ManySearch import ManySearch


class SequentialAStar(ManySearch):
  def __init__(self, grid, n, w1, w2, heuristics, i=-1):
    super().__init__(grid, n, w1, w2, heuristics, i)

    # Cell list of 2D arrays, Closed list of 2D arrays, Sprime tracker list of 2D arrays
    self.cells = np.array([np.asmatrix([[AlgoCell(x, y) for y in range(Constants.COLUMNS)] for x in range(Constants.ROWS)]) for z in range(n)])
    self.closedList = np.array([np.asmatrix([[False for y in range(Constants.COLUMNS)] for x in range(Constants.ROWS)]) for z in range(n)])
    self.tracker = np.array([np.asmatrix([[False for y in range(Constants.COLUMNS)] for x in range(Constants.ROWS)]) for z in range(n)])


  # Start the algoirthm. Searches for the best path based on the heuristic.
  def search(self):
    startTime = int(round(time.time() * 1000))  # Get time when the algorithm started

    # Initial setup
    for i in range(self.n):
      priority = self.Key(self.start, i)

      self.cells[i][self.start.X, self.start.Y].G = 0
      self.cells[i][self.goal.X, self.goal.Y].G = math.inf
      self.cells[i][self.start.X, self.start.Y].Parent = None
      self.cells[i][self.goal.X, self.goal.Y].Parent = None
      self.cells[i][self.start.X, self.start.Y].Priority = priority

      self.fringe[i].push(priority, self.start)
      self.openList[i][self.start.X, self.start.Y] = True

    # Run algorithm
    while self.fringe[0].peek()[0] < math.inf:
      # Run search in a round-robin manner for the corresponding queue
      for i in range(1, self.n):
        # Check if path is found using non-achor search processes
        if (self.fringe[i].peek()[0] <= self.w2 * self.fringe[0].peek()[0]):
          if (self.cells[i][self.goal.X, self.goal.Y].G <= self.fringe[i].peek()[0]):
            if (self.cells[i][self.goal.X, self.goal.Y].G < math.inf):
              self.time = int(round(time.time() * 1000)) - startTime
              self.pathlength = self.cells[i][self.goal.X, self.goal.Y].G
              self.tracePath(self.cells[i])
              return True

          # G value of ith search process is further away than anchor
          else:
            s = self.fringe[i].pop()[1]
            self.openList[i][s.X, s.Y] = False
            self.ExpandState(s, i)
            self.nodeexpanded += 1
            self.closedList[i][s.X, s.Y] = True

        # Anchor priority is higher
        else:
          # Check if path found using anchor search processes
          if (self.cells[0][self.goal.X, self.goal.Y].G <= self.fringe[0].peek()[0]):
            if (self.cells[0][self.goal.X, self.goal.Y].G < math.inf):
              self.time = int(round(time.time() * 1000)) - startTime
              self.pathlength = self.cells[0][self.goal.X, self.goal.Y].G
              self.tracePath(self.cells[0])
              return True

          # Anchor priority is higher but G value is lower
          else:
            s = self.fringe[0].pop()[1]
            self.openList[0][s.X, s.Y] = False
            self.ExpandState(s, 0)
            self.nodeexpanded += 1
            self.closedList[0][s.X, s.Y] = True

    # No path found
    self.time = int(round(time.time() * 1000)) - startTime
    return False


  # Expand the state
  def ExpandState(self, s, i):
    # Get all the successors for s
    for sp in Formulas.Successors(s, self.grid):
      # Get cost
      cost = self.cells[i][s.X, s.Y].G + Formulas.PathCost(s, sp)
      
      # Get the old priority for removal
      old_priority = self.cells[i][sp.X, sp.Y].Priority

      # Check if sprime was generated in ith search
      if (self.tracker[i][sp.X, sp.Y] == False):
        self.cells[i][sp.X, sp.Y].G = math.inf
        self.cells[i][sp.X, sp.Y].Parent = None
        self.tracker[i][sp.X, sp.Y] = True

      # Good path found, set the parent and G value
      if (self.cells[i][sp.X, sp.Y].G > cost):
        self.cells[i][sp.X, sp.Y].G = cost
        self.cells[i][sp.X, sp.Y].Parent = s

        # Check if in closed list and fringe. If in fringe, remove it
        if (self.closedList[i][sp.X, sp.Y] == False):
          if (self.openList[i][sp.X, sp.Y] == True):
            self.fringe[i].remove((old_priority, sp))

          # Insert/Update sprime with new priority
          priority = self.Key(sp, i)
          self.cells[i][sp.X, sp.Y].Priority = priority
          self.fringe[i].push(priority, sp)
          self.openList[i][sp.X, sp.Y] = True


  # Get the key for priority
  def Key(self, s, i):
    self.cells[i][s.X, s.Y].H = self.heuristics[i](s, self.goal)
    self.cells[i][s.X, s.Y].F = self.cells[i][s.X, s.Y].G + self.cells[i][s.X, s.Y].H
    return self.cells[i][s.X, s.Y].G + self.w1 * self.cells[i][s.X, s.Y].H
