import math, time
import Algorithms.Base.Formulas as Formulas
from Algorithms.Base.SingleSearch import SingleSearch


class AStar(SingleSearch):
  def __init__(self, grid, start, goal):
    super().__init__(grid, start, goal)
    

  # Start the algoirthm. Searches for the best path based on the heuristic.
  def search(self):
    startTime = int(round(time.time() * 1000))  # Get when the algorithm started

    # Set distance from start and set parent to itself. Push to the heap with heuristic as priority
    self.start.G = 0
    self.start.H = self.Heuristic(self.start)
    self.start.F = self.start.G + self.start.H
    self.start.Parent = self.start
    self.start.Priority = self.start.F
    self.fringe.push(self.start.Priority, self.start)

    # Loop until goal is found or fringe is empty (no more nodes to expand)
    while(self.fringe.isEmpty() == False):

      # Get highest priority cell (lowest number) and set that position to False in the open list
      s = self.fringe.pop()[1];
      self.openList[s.X, s.Y] = False

      # Goal found, stop the loop
      if(s == self.goal):
        self.time = int(round(time.time() * 1000)) - startTime
        return True

      # Add it to visited list
      self.nodeexpanded += 1
      self.closedList[s.X, s.Y] = True

      # Loop for all neighbors around the popped cell ('s') and check if already visited
      for sprime in Formulas.Successors(s, self.grid):
        if(self.closedList[sprime.X, sprime.Y] == False):
          if(self.openList[sprime.X, sprime.Y] == False):
            sprime.G = math.inf
            sprime.Parent = None

          self.UpdateVertex(s, sprime)

    # No path found
    self.time = int(round(time.time() * 1000)) - startTime
    return False


  # Update a cell's G value and its parent
  def UpdateVertex(self, s, sprime):
    # Get the cost to traverse + distance to root
    cost = s.G + Formulas.PathCost(s, sprime)

    # Check if good path found
    if(cost < sprime.G):
      # Get old cost for removal
      old_priority = sprime.Priority

      # Set all the updated values for cell
      sprime.H = self.Heuristic(sprime)
      sprime.G = cost
      sprime.F = sprime.G + sprime.H
      sprime.Parent = s 

      # Remove it from fringe as it has been updated
      if(self.openList[sprime.X, sprime.Y] == True):
        self.fringe.remove((old_priority, sprime))

      # Push the updated cell in
      sprime.Priority = sprime.F
      self.fringe.push(sprime.Priority, sprime)
      self.openList[sprime.X, sprime.Y] = True


  # Heuristic to guide the A* along the optimal path
  def Heuristic(self, s):
    min_XY = min(abs(s.X - self.goal.X), abs(s.Y - self.goal.Y))
    max_XY = max(abs(s.X - self.goal.X), abs(s.Y - self.goal.Y))

    return (1.41421356237 * min_XY) + max_XY - min_XY
