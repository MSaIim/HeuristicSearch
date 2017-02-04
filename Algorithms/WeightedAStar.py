import math, time
import Algorithms.Formulas as Formulas
from Algorithms.Search import Search

class WeightedAStar(Search):
	def __init__(self, grid, start, goal, heuristic, weight):
		super().__init__(grid, start, goal)
		self.weight = weight
		self.Heuristic = heuristic


	# Start the algoirthm. Searches for the best path based on the heuristic.
	def search(self):
		startTime = int(round(time.time() * 1000))	# Get when the algorithm started

		# Set distance from start and set parent to itself. Push to the heap with heuristic as priority
		self.start.G = 0
		self.start.Parent = self.start
		self.fringe.push(self.start, self.start.G + self.weight * self.Heuristic(self.start, self.goal, self.grid))

		# Loop until goal is found or fringe is empty (no more nodes to expand)
		while(self.fringe.isEmpty() == False):
			
			# Get highest priority cell (lowest number)
			s = self.fringe.pop()[1];
			self.openList[s.X, s.Y] = False

			# Goal found, stop the loop
			if(s == self.goal):
				self.time = int(round(time.time() * 1000)) - startTime
				return True

			# Add it to visited list
			self.closedList[s.X, s.Y] = True

			# Loop for all neighbors around the popped cell ('s') and check if already visited
			for sprime in Formulas.Successors(s, self.grid):
				if(self.closedList[sprime.X, sprime.Y] == False):
					if(self.openList[sprime.X, sprime.Y] == False):			# ** MAY NOT NEED THESE LINES **
						sprime.G = math.inf									# We set the default values when
						sprime.Parent = None								# we first create the cells.

					self.updateVertex(s, sprime)

		# No path found
		self.time = int(round(time.time() * 1000)) - startTime
		return False


	# Update a cell's G value and its parent
	def updateVertex(self, s, sprime):
		# Get the cost to traverse + distance to root
		cost = s.G + Formulas.PathCost(s, sprime)	

		# Check if its admissible
		if(cost < sprime.G):
			sprime.G = cost 		# Update the distance from start
			sprime.Parent = s 		# Set the parent to previous cell

			# Remove it from fringe as it has been updated
			if(self.openList[sprime.X, sprime.Y]):
				self.fringe.remove(sprime)

			# Push the updated cell in
			self.openList[sprime.X, sprime.Y] = True
			self.fringe.push(sprime, sprime.G + self.Heuristic(sprime, self.goal, self.grid))
