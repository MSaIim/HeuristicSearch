import math, time
import Algorithms.Base.Formulas as Formulas
from Algorithms.Base.Search import Search

class UniformCost(Search):
	def __init__(self, grid, start, goal):
		super().__init__(grid, start, goal)

		
	# Start the algoirthm. Searches for the best path based on the heuristic.
	def search(self):
		startTime = int(round(time.time() * 1000))	# Get when the algorithm started

		# Set distance from start and set parent to itself. Push to the heap with heuristic as priority
		self.start.G = 0
		self.start.Parent = self.start
		self.fringe.push(self.start, self.start.G)

		# Loop until goal is found or fringe is empty (no more nodes to expand)
		while(self.fringe.isEmpty() == False):

			# Get highest priority cell (lowest number) and set that position to False in the open list
			s = self.fringe.pop()[1];
			self.openList[s.X, s.Y] = False

			# Goal found, stop the loop
			if(s == self.goal):
				self.time = int(round(time.time() * 1000)) - startTime

				# For benchmarks
				for row in range(120):
					for col in range(160):
						if self.closedList[row, col] == True:
							self.nodeexpanded += 1
							
				return True

			# Add it to visited list
			self.closedList[s.X, s.Y] = True

			# Loop for all neighbors around the popped cell ('s') and check if already visited
			for sprime in Formulas.Successors(s, self.grid):
				if(self.closedList[sprime.X, sprime.Y] == False):
					if(self.openList[sprime.X, sprime.Y] == False):
						sprime.G = math.inf
						sprime.Parent = None

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
			sprime.G = cost 	# Update the distance from start
			sprime.Parent = s 		# Set the parent to previous cell

			# Remove it from fringe as it has been updated
			if(self.openList[sprime.X, sprime.Y]):
				self.fringe.remove(sprime)

			# Push the updated cell in
			self.openList[sprime.X, sprime.Y] = True
			self.fringe.push(sprime, sprime.G)
