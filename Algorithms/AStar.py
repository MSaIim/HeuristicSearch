import numpy as np
from Grid.Cell import Cell
from Algorithms.Heap import PriorityQueue
from Algorithms.Search import Search
from Algorithms.Formulas import Formulas

class AStar(Search):
	def __init__(self, grid, start, goal):
		super().__init__(grid, start, goal)
		self.fringe = PriorityQueue()


	def search(self):
		closed = []
		closedAppend = closed.append

		self.start.G = 0
		self.start.Parent = self.start
		self.fringe.push(self.start, self.start.G + Formulas.AStarHeuristic(self.start, self.goal))

		while(self.fringe.isEmpty() == False):
			s = self.fringe.pop();
			closedAppend(s)

			for sprime in Formulas.Successors(s, self.grid):
				if(sprime == self.goal):
					sprime.Parent = s
					return self.getPath()

				if(sprime not in closed):
					if(self.fringe.contains(sprime) == False):
						sprime.G = float("inf")
						sprime.Parent = None

					self.updateVertex(s, sprime)

		return None


	def updateVertex(self, s, sprime):
		if(s.G + Formulas.PathCost(s, sprime) < sprime.G):
			sprime.G = s.G + Formulas.PathCost(s, sprime)
			sprime.Parent = s

			if(self.fringe.contains(sprime)):
				self.fringe.remove(sprime)

			self.fringe.push(sprime, sprime.G + Formulas.AStarHeuristic(sprime, self.goal))
