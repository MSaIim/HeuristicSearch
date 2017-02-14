import math, time
import numpy as np
import Utilities.Constants as Constants
import Algorithms.Base.Formulas as Formulas
from Algorithms.Base.ManySearch import ManySearch


class IntegratedAStar(ManySearch):
  def __init__(self, grid, start, goal, n, w1, w2, heuristics):
    super().__init__(grid, start, goal, n, w1, w2, heuristics)

    # For benchmarks
    self.nodeExAnchor = 0
    self.nodeExInadm = 0

    # Array of grids
    self.cells = grid

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
              return True

          # G value of ith search process is further away than anchor
          else:
            s = self.fringe[i].pop()[1]
            self.ExpandState(s, i)
            self.nodeExInadm += 1
            self.closedInadm[s.X, s.Y] = True

        # Anchor priority is higher
        else:
          # Check if path found using anchor search processes
          if (self.cells[self.goal.X, self.goal.Y].G <= self.fringe[0].peek()[0]):
            if (self.cells[self.goal.X, self.goal.Y].G < math.inf):
              self.time = int(round(time.time() * 1000)) - startTime
              return True

          # Anchor priority is higher but G value is lower
          else:
            s = self.fringe[0].pop()[1]
            self.ExpandState(s, 0)
            self.nodeExAnchor += 1
            self.closedAnchor[s.X, s.Y] = True

    # No path found
    self.time = int(round(time.time() * 1000)) - startTime
    return False


  # Expand the state
  def ExpandState(self, s, i):
    # Remove s from all fringes
    s_priority = self.Key(s, i) # Get old s priority
    for i in range(self.n):
      self.fringe[i].remove((s_priority, s))
      self.openList[i][s.X, s.Y] = False
      print("1")

      # Get all the successors for s
      for sp in Formulas.Successors(s, self.grid):
        # Get the total cost from s to sp
        cost = self.cells[s.X, s.Y].G + Formulas.PathCost(s, sp)
        print("2")
        # Check if sprime was generated
        if (self.tracker[sp.X, sp.Y] == False):
          self.cells[sp.X, sp.Y].G = math.inf
          self.cells[sp.X, sp.Y].Parent = None
          print("3")

        # Good path found, set the parent and G value
        sp_priority = self.Key(sp, i) # Get old sprime priority
        if(self.cells[sp.X, sp.Y].G > cost):
          self.cells[sp.X, sp.Y].G = cost
          self.cells[sp.X, sp.Y].Parent = s
          print("4")

          # Check if in closed anchor list and anchor fringe.
          if (self.closedAnchor[sp.X, sp.Y] == False):
            if (self.openList[0][sp.X, sp.Y] == True):
              self.fringe[0].remove((sp_priority, sp))

            # Insert/Update sprime with new priority
            self.fringe[0].push(self.Key(sp, 0), sp)
            self.openList[0][sp.X, sp.Y] = True

            # Check if in closed inadmisslbe list
            if (self.closedInadm[sp.X, sp.Y] == False):
              for i in range(1, self.n):
                if (self.Key(sp, i) <= self.w2 * self.Key(sp, 0)):
                  if (self.openList[i][sp.X, sp.Y] == True):
                    self.fringe[i].remove((sp_priority, sp))
                    print("6")

                  # Insert/Update sprime with new priority
                  self.fringe[i].push(self.Key(sp, i), sp)
                  self.openList[i][sp.X, sp.Y] = True


  # Get the key for priority
  def Key(self, s, i):
    return self.cells[s.X, s.Y].G + self.w1 * self.heuristics[i](s, self.goal)
