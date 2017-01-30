from Grid.Cell import Cell
from Algorithms.Heap import PriorityQueue
from Algorithms.Search import Search
from Algorithms.Formulas import Formulas
from copy import deepcopy

class AStar(Search):
	def __init__(self, grid, start, goal):
		super().__init__(grid, start, goal)

		self.fringe = PriorityQueue()
		self.closed = []


	def search(self):
		self.start.G = 0
		self.start.parent = self.start
		self.fringe.push(self.start, self.start.G + Formulas.AStarHeuristic(self.start, self.goal))

		while(self.fringe.isEmpty() == False):
			# Get the highest priority item (lowest number)
			s = self.fringe.pop();

			# Goal has been found
			if(s == self.goal):
				print("done")
				return True

			# Add to visited list
			self.closed.append(s)

			# Get the surrounding cells of 's' (Non-Blocked) and check if in lists
			for sprime in Formulas.Successors(s, self.grid):
				if(sprime not in self.closed):
					if(self.fringe.contains(sprime) == False):
						sprime.G = float("inf")
						sprime.parent = None

					# Update the vertex values
					self.updateVertex(s, sprime)

		# Goal not found
		return False


	# Update the vertex values and update the fringe
	def updateVertex(self, s, sprime):
		# Check if current cell is the faster path than the neighboring cell
		if(s.G + Formulas.PathCost(s, sprime) < sprime.G):
			sprime.G = s.G + Formulas.PathCost(s, sprime)	# Update the distance to goal
			sprime.Parent = s 								# Set the parent as current cell

			# Remove neighboring cell from the fringe
			if(self.fringe.contains(sprime)):
				self.fringe.remove(sprime)

			# Push neighboring cell with updated priority
			self.fringe.push(sprime, sprime.G + Formulas.AStarHeuristic(sprime, self.goal))
