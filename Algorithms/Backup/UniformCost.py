import math, time
import Algorithms.Formulas as Formulas
from Algorithms.Search import Search

class UniformCost(Search):
	def __init__(self, grid, start, goal):
		super().__init__(grid, start, goal)
		

	def search(self):
		# Start algorithm
		startTime = int(round(time.time() * 1000))

		# Push start to fringe
		self.start.Parent = self.start
		self.fringe.push(self.start, 0)

		# Loop until goal is found or fringe is empty (no more nodes to expand)
		while(self.fringe.isEmpty() == False):

			# Get highest priority cell (lowest number)
			cost, s = self.fringe.pop();
			self.openList[s.X, s.Y] = False

			# Goal found, stop the loop
			if(s == self.goal):
				self.time = int(round(time.time() * 1000)) - startTime
				return True

			# Add it to visited list
			self.closedList[s.X, s.Y] = True

			# Expand the current node 's' to get its children to add to the fringe
			for sprime in Formulas.Successors(s, self.grid):
				total_cost = cost + Formulas.PathCost(s, sprime)	

				# Check if in closed or the fringe
				if(self.closedList[sprime.X, sprime.Y] == False and self.openList[sprime.X, sprime.Y] == False):
					sprime.Parent = s
					self.openList[sprime.X, sprime.Y] = True
					self.fringe.push(sprime, total_cost)

				# Check if in fringe and if child path cost is greater
				elif(self.openList[sprime.X, sprime.Y] and total_cost > cost):
					sprime.Parent = s
					self.fringe.remove(sprime)
					self.fringe.push(sprime, total_cost)


		# No path found
		self.time = int(round(time.time() * 1000)) - startTime
		return False
