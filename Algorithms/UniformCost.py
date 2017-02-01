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
		