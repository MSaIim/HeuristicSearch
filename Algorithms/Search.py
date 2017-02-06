import numpy as np
import Algorithms.Heap
import Utilities.Constants as Constants
from abc import ABC, abstractmethod

# Abstract class Search
class Search(ABC):
	def __init__(self, grid, start, goal):
		self.grid = grid
		self.start = start
		self.goal = goal
		self.time = 0

		# For benchmarks
		# self.pathlength = 0
		# self.nodeexpanded = 0

		# Min Heap to hold nodes that might be expanded
		self.fringe = Algorithms.Heap.PriorityQueue()

		# 2D array of booleans to know which cell is in the fringe
		self.openList = np.asmatrix([[False for y in range(Constants.COLUMNS)] for x in range(Constants.ROWS)])
		self.closedList = np.asmatrix([[False for y in range(Constants.COLUMNS)] for x in range(Constants.ROWS)])


	# All Search algorithms should have their own way to find the path
	@abstractmethod
	def search(self):
		pass


	# Get the path from the start to the goal
	def getPath(self):
		searchPath = []
		done = False
		cell = self.goal

		while done == False:
			searchPath.append(cell)

			if(cell == self.start):
				done = True

			cell = cell.Parent

		# For benchmarks
		# self.pathlength = self.goal.G
		return searchPath


	# For use with the "as" statement in the "with" clause
	def __enter__(self):
		return self


	# What to do after "with" statement is done
	def __exit__(self, *err):
		del self
