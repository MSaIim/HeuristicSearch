import math, Algorithms.Heap
import Algorithms.Formulas as Formulas
from Algorithms.Search import Search

class AStarWeighted(Search):
	def __init__(self, grid, start, goal, weight):
		super().__init__(grid, start, goal)
		self.fringe = Algorithms.Heap.PriorityQueue()
		self.weight = weight


	def search(self):
		closed = []
		closedAppend = closed.append

		self.start.G = 0
		self.start.Parent = self.start
		self.fringe.push(self.start, self.start.G + self.weight * Formulas.AStarHeuristic(self.start, self.goal))

		while(self.fringe.isEmpty() == False):
			s = self.fringe.pop();
			closedAppend(s)

			for sprime in Formulas.Successors(s, self.grid):
				if(sprime == self.goal):
					sprime.G = s.G + Formulas.PathCost(s, sprime)
					sprime.Parent = s
					return self.getPath()

				if(sprime not in closed):
					if(self.fringe.contains(sprime) == False):
						sprime.G = math.inf
						sprime.Parent = None

					self.updateVertex(s, sprime)

		return None


	def updateVertex(self, s, sprime):
		cost = Formulas.PathCost(s, sprime)

		if(s.G + cost < sprime.G):
			sprime.G = s.G + cost
			sprime.Parent = s

			if(self.fringe.contains(sprime)):
				self.fringe.remove(sprime)

			self.fringe.push(sprime, sprime.G + self.weight * Formulas.AStarHeuristic(sprime, self.goal))
