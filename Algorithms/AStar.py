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

		print(self.fringe)

		while(self.fringe.isEmpty() == False):
			s = self.fringe.pop();

			if(s == self.goal):
				print("done")
				return True

			self.closed.append(s)

			for sprime in Formulas.Successors(s, self.grid):
				if(sprime not in self.closed):
					if(self.fringe.contains(sprime) == False):
						sprime.G = float("inf")
						sprime.parent = None

					self.updateVertex(s, sprime)

		return False


	def updateVertex(self, s, sprime):
		if(s.G + Formulas.PathCost(s, sprime) < sprime.G):
			sprime.G = s.G + Formulas.PathCost(s, sprime)
			sprime.Parent = s

			if(self.fringe.contains(sprime)):
				self.fringe.remove(sprime)

			self.fringe.push(sprime, sprime.G + Formulas.AStarHeuristic(sprime, self.goal))
