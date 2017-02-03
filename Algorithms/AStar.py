import numpy as np
import math, time, Algorithms.Heap
import Algorithms.Formulas as Formulas
import Utilities.Constants as Constants
from Algorithms.Search import Search

class AStar(Search):
	def __init__(self, grid, start, goal):
		super().__init__(grid, start, goal)
		self.time = 0
		self.fringe = Algorithms.Heap.PriorityQueue()

		# 2D array of booleans to know which cell is in the fringe
		self.openList = np.asmatrix([[False for y in range(Constants.COLUMNS)] for x in range(Constants.ROWS)])

		
	# Start the algoirthm. Searches for the best path based on the heuristic.
	def search(self):
		startTime = int(round(time.time() * 1000))	# Get when the algorithm started

		# 2D array of booleans to know which cell has been visited
		closedList = np.asmatrix([[False for y in range(Constants.COLUMNS)] for x in range(Constants.ROWS)])

		# Set distance from start and set parent to itself. Push to the heap with heuristic as priority
		self.start.G = 0
		self.start.Parent = self.start
		self.fringe.push(self.start, self.start.G + self.Heuristic(self.start))

		# Loop until goal is found or fringe is empty (no more nodes to expand)
		while(self.fringe.isEmpty() == False):

			# Get highest priority cell (lowest number) and set that position to False in the open list
			s = self.fringe.pop()[1];
			self.openList[s.X, s.Y] = False

			# Goal found, stop the loop
			if(s == self.goal):
				self.time = int(round(time.time() * 1000)) - startTime
				return True

			# Add it to visited list
			closedList[s.X, s.Y] = True

			# Loop for all neighbors around the popped cell ('s') and check if already visited
			for sprime in Formulas.Successors(s, self.grid):
				if(closedList[sprime.X, sprime.Y] == False):
					if(self.openList[sprime.X, sprime.Y] == False):		# ** MAY NOT NEED THESE LINES **
						sprime.G = math.inf								# We set the default values when
						sprime.Parent = None							# we first create the cells.

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
			if(self.openList[sprime.X, sprime.Y]):
				self.fringe.remove(sprime)

			# Push the updated cell in
			self.openList[sprime.X, sprime.Y] = True
			self.fringe.push(sprime, sprime.G + self.Heuristic(sprime))


	# Heuristic to guide the A* along the optimal path
	def Heuristic(self, s):
		a = math.sqrt(2)
		min_XY = min(abs(s.X - self.goal.X), abs(s.Y - self.goal.Y))
		max_XY = max(abs(s.X - self.goal.X), abs(s.Y - self.goal.Y))

		return (a * min_XY) + max_XY - min_XY
