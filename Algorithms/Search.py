from abc import ABC, abstractmethod

class Search(ABC):
	def __init__(self, grid, start, goal):
		self.grid = grid
		self.start = self.getCell(start)
		self.goal = self.getCell(goal)

	@abstractmethod
	def search(self):
		pass

	def getCell(self, point):
		return self.grid[point.x, point.y]

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
