import numpy as np
import math, time, Algorithms.Heap
import Algorithms.Formulas as Formulas
import Utilities.Constants as Constants
from Algorithms.Search import Search

class UniformCost(Search):
	def __init__(self, grid, start, goal):
		super().__init__(grid, start, goal)
		self.time = 0
		self.fringe = Algorithms.Heap.PriorityQueue()
		

	def search(self):
		# Start algorithm
		startTime = int(round(time.time() * 1000))
		
		# 2D array of booleans to know which cell is in the fringe or closed list
		openList = np.asmatrix([[False for y in range(Constants.COLUMNS)] for x in range(Constants.ROWS)])
		closedList = np.asmatrix([[False for y in range(Constants.COLUMNS)] for x in range(Constants.ROWS)])

		# Push start to fringe
		self.fringe.push(self.start, 0)

		# Loop until goal is found or fringe is empty (no more nodes to expand)
		while(self.fringe.isEmpty() == False):

			# Get highest priority cell (lowest number)
			cost, s = self.fringe.pop();
			openList[s.X, s.Y] = False

			# Goal found, stop the loop
			if(s == self.goal):
				self.time = int(round(time.time() * 1000)) - startTime
				return True

			# Add it to visited list
			closedList[s.X, s.Y] = True

			# Expand the current node 's' to get its children to add to the fringe
			for sprime in Formulas.Successors(s, self.grid):
				total_cost = cost + Formulas.PathCost(s, sprime)	

				# Check if in closed or the fringe
				if(closedList[sprime.X, sprime.Y] == False and openList[sprime.X, sprime.Y] == False):
					sprime.Parent = s
					openList[sprime.X, sprime.Y] = True
					self.fringe.push(sprime, total_cost)

				# Check if in fringe and if child path cost is greater
				elif(openList[sprime.X, sprime.Y] and total_cost > cost):
					sprime.Parent = s
					self.fringe.remove(sprime)
					self.fringe.push(sprime, total_cost)


		# No path found
		self.time = int(round(time.time() * 1000)) - startTime
		return False
