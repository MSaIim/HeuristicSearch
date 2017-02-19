import math, time
import numpy as np
from Grid.Cell import AlgoCell
import Utilities.Constants as Constants
import Algorithms.Base.Formulas as Formulas
from Algorithms.Base.ManySearch import ManySearch


class IntegratedAStar(ManySearch):
  def __init__(self, grid, n, w1, w2, heuristics, i=-1):
    super().__init__(grid, n, w1, w2, heuristics, i)

    # Array of grids
    self.cells = np.asmatrix([[AlgoCell(x, y) for y in range(Constants.COLUMNS)] for x in range(Constants.ROWS)])

    # Closed list for anchor and another for inadmissible heuristics
    self.closedAnchor = np.asmatrix([[False for y in range(Constants.COLUMNS)] for x in range(Constants.ROWS)])
    self.closedInadm = np.asmatrix([[False for y in range(Constants.COLUMNS)] for x in range(Constants.ROWS)])
    
    # Array to keep track of sprimes
    self.tracker = np.asmatrix([[False for y in range(Constants.COLUMNS)] for x in range(Constants.ROWS)])


  # Start the algoirthm. Searches for the best path based on the heuristic.
  def search(self):
    startTime = int(round(time.time() * 1000))  # Get time when the algorithm started

    # Initial setup
    self.cells[self.start.X, self.start.Y].G = 0
    self.cells[self.goal.X, self.goal.Y].G = math.inf
    self.cells[self.start.X, self.start.Y].Parent = None
    self.cells[self.goal.X, self.goal.Y].Parent = None

    for i in range(self.n):
      self.fringe[i].push(self.Key(self.start, i), self.start)
      self.openList[i][self.start.X, self.start.Y] = True

    # Run algorithm
    while self.fringe[0].peek()[0] < math.inf:
      # Run search in a round-robin manner for the corresponding queue
      for i in range(1, self.n):
        # Check if path is found using non-achor search processes
        if (self.fringe[i].peek()[0] <= self.w2 * self.fringe[0].peek()[0]):
          if (self.cells[self.goal.X, self.goal.Y].G <= self.fringe[i].peek()[0]):
            if (self.cells[self.goal.X, self.goal.Y].G < math.inf):
              self.time = int(round(time.time() * 1000)) - startTime
              self.pathlength = self.cells[self.goal.X, self.goal.Y].G
              self.tracePath(self.cells)
              return True

          # G value of ith search process is further away than anchor
          else:
            s = self.fringe[i].pop()[1]
            self.openList[i][s.X, s.Y] = False
            self.ExpandState(s, i)
            self.nodeexpanded += 1
            self.closedInadm[s.X, s.Y] = True

        # Anchor priority is higher
        else:
          # Check if path found using anchor search processes
          if (self.cells[self.goal.X, self.goal.Y].G <= self.fringe[0].peek()[0]):
            if (self.cells[self.goal.X, self.goal.Y].G < math.inf):
              self.time = int(round(time.time() * 1000)) - startTime
              self.pathlength = self.cells[self.goal.X, self.goal.Y].G
              self.tracePath(self.cells)
              return True

          # Anchor priority is higher but G value is lower
          else:
            s = self.fringe[0].pop()[1]
            self.openList[0][s.X, s.Y] = False
            self.ExpandState(s, 0)
            self.nodeexpanded += 1
            self.closedAnchor[s.X, s.Y] = True

    # No path found
    self.time = int(round(time.time() * 1000)) - startTime
    return False


  # Expand the state
  def ExpandState(self, s, i):
    # Remove s from all fringes
    s_tuple = (self.Key(s, i), s) # Get old s priority
    for i in range(self.n):
      self.fringe[i].remove(s_tuple)
      self.openList[i][s.X, s.Y] = False

      # Get all the successors for s
      for sp in Formulas.Successors(s, self.grid):
        # Get the total cost from s to sp
        cost = self.cells[s.X, s.Y].G + Formulas.PathCost(s, sp)

        # Check if sprime was generated
        if (self.tracker[sp.X, sp.Y] == False):
          self.cells[sp.X, sp.Y].G = math.inf
          self.cells[sp.X, sp.Y].Parent = None
          self.tracker[sp.X, sp.Y] = True

        # Good path found, set the parent and G value
        sp_tuple = (self.Key(sp, i), sp) # Get old sprime priority
        if(self.cells[sp.X, sp.Y].G > cost):
          self.cells[sp.X, sp.Y].G = cost
          self.cells[sp.X, sp.Y].Parent = s

          # Check if in closed anchor list and anchor fringe.
          if (self.closedAnchor[sp.X, sp.Y] == False):
            if (self.openList[0][sp.X, sp.Y] == True):
              self.fringe[0].remove(sp_tuple)

            # Insert/Update sprime with new priority
            self.fringe[0].push(self.Key(sp, 0), sp)
            self.openList[0][sp.X, sp.Y] = True

            # Check if in closed inadmisslbe list
            if (self.closedInadm[sp.X, sp.Y] == False):
              for i in range(1, self.n):
                if (self.Key(sp, i) <= self.w2 * self.Key(sp, 0)):
                  if (self.openList[i][sp.X, sp.Y] == True):
                    self.fringe[i].remove(sp_tuple)

                  # Insert/Update sprime with new priority
                  self.fringe[i].push(self.Key(sp, i), sp)
                  self.openList[i][sp.X, sp.Y] = True


  # Get the key for priority
  def Key(self, s, i):
    self.cells[s.X, s.Y].H = self.heuristics[i](s, self.goal)
    self.cells[s.X, s.Y].F = self.cells[s.X, s.Y].G + self.cells[s.X, s.Y].H
    return self.cells[s.X, s.Y].G + self.w1 * self.cells[s.X, s.Y].H
    

  # Get the path from the start to the goal
  def getPath(self):
    searchPath = []
    append = searchPath.append
    cell = self.cells[self.goal.X, self.goal.Y]

    # Trace path back to start
    while cell is not self.start:
      append(cell)
      cell = self.cells[cell.X, cell.Y].Parent

    # Assign f, g, h values
    for row in range(Constants.ROWS):
      for col in range(Constants.COLUMNS):
        self.grid[row, col].F = self.cells[row, col].F
        self.grid[row, col].G = self.cells[row, col].G
        self.grid[row, col].H = self.cells[row, col].H

    # For benchmarks
    self.pathlength = self.cells[self.goal.X, self.goal.Y].G

    return searchPath
