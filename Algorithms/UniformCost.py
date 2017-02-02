import math, time, Algorithms.Heap
import Algorithms.Formulas as Formulas
from Algorithms.Search import Search

class UniformCost(Search):
	def __init__(self, grid, start, goal):
		super().__init__(grid, start, goal)
		self.time = 0
		self.fringe = Algorithms.Heap.PriorityQueue()
		

	def search(self):
		# Start algorithm
		startTime = int(round(time.time() * 1000))
		
		# Start algorithm
		closed = []
		closedAppend = closed.append

		# Push start to fringe
		self.fringe.push(self.start, 0)

		# Loop until goal is found or fringe is empty (no more nodes to expand)
		while(self.fringe.isEmpty() == False):

			# Get highest priority cell (lowest number)
			cost, s = self.fringe.pop();

			# Goal found, stop the loop
			if(s == self.goal):
				self.time = int(round(time.time() * 1000)) - startTime
				return True

			# Add it to visited list
			closedAppend(s)

			# Expand the current node 's' to get its children to add to the fringe
			for sprime in Formulas.Successors(s, self.grid):
				total_cost = cost + Formulas.PathCost(s, sprime)	

				# Check if in closed or the fringe
				if(sprime not in closed and self.fringe.contains(sprime) == False):
					sprime.Parent = s
					self.fringe.push(sprime, total_cost)

				# Check if in fringe and if child path cost is greater
				elif(self.fringe.contains(sprime) and total_cost > cost):
					sprime.Parent = s
					self.fringe.remove(sprime)
					self.fringe.push(sprime, total_cost)


		# No path found
		self.time = int(round(time.time() * 1000)) - startTime
		return False
