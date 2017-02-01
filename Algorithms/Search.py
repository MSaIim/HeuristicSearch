from abc import ABC, abstractmethod

class Search(ABC):
	def __init__(self, grid, start, goal):
		self.grid = grid
		self.start = start
		self.goal = goal

	@abstractmethod
	def search(self):
		pass

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
