import math, time, Algorithms.Heap
import Algorithms.Formulas as Formulas
from Algorithms.Search import Search

class WeightedAStar(Search):
	def __init__(self, grid, start, goal, heuristic, weight):
		super().__init__(grid, start, goal)
		self.time = 0
		self.fringe = Algorithms.Heap.PriorityQueue()
		self.weight = weight
		self.Heuristic = heuristic


	# Start the algoirthm. Searches for the best path based on the heuristic.
	def search(self):
		startTime = int(round(time.time() * 1000))	# Get when the algorithm started

		# Start algorithm
		closed = []
		closedAppend = closed.append

		# Set distance from start and set parent to itself. Push to the heap with heuristic as priority
		self.start.G = 0
		self.start.Parent = self.start
		self.fringe.push(self.start, self.start.G + self.weight * self.Heuristic(self.start, self.goal, self.grid))

		# Loop until goal is found or fringe is empty (no more nodes to expand)
		while(self.fringe.isEmpty() == False):
			
			# Get highest priority cell (lowest number)
			s = self.fringe.pop();

			# Goal found, stop the loop
			if(s == self.goal):
				self.time = int(round(time.time() * 1000)) - startTime
				return True

			# Add it to visited list
			closedAppend(s)

			# Loop for all neighbors around the popped cell ('s') and check if already visited
			for sprime in Formulas.Successors(s, self.grid):
				if(sprime not in closed):
					if(self.fringe.contains(sprime) == False):		# ** MAY NOT NEED THESE LINES **
						sprime.G = math.inf							# We set the default values when
						sprime.Parent = None						# we first create the cells.
					self.updateVertex(s, sprime)

		# No path found
		self.time = int(round(time.time() * 1000)) - startTime
		return False


	# Update a cell's G value and its parent
	def updateVertex(self, s, sprime):
		# Get the cost to traverse
		cost = Formulas.PathCost(s, sprime)	

		# Check if its admissible
		if(s.G + cost < sprime.G):
			sprime.G = s.G + cost 	# Update the distance from start
			sprime.Parent = s 		# Set the parent to previous cell

			# Remove it from fringe as it has been updated
			if(self.fringe.contains(sprime)):
				self.fringe.remove(sprime)

			# Push the updated cell in
			self.fringe.push(sprime, sprime.G + self.Heuristic(sprime, self.goal, self.grid))
