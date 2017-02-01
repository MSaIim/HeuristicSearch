from abc import ABC, abstractmethod

# Abstract class Search
class Search(ABC):
	def __init__(self, grid, start, goal):
		self.grid = grid
		self.start = start
		self.goal = goal

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

		return searchPath


	# For use with the "as" statement in the "with" clause
	def __enter__(self):
		return self


	# What to do after "with" statement is done
	def __exit__(self, *err):
		del self