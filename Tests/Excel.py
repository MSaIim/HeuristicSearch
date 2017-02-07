import xlwt, math
from tkinter import messagebox
from Grid.Grid import Grid
from Algorithms.AStar import AStar
from Algorithms.WeightedAStar import WeightedAStar
from Algorithms.UniformCost import UniformCost


class Test(object):
	def __init__(self):
		self.grid = Grid()
		#self.grid.save("Resources/maps/Map05.map")
		self.grid.load("Resources/maps/Map01.map")

		self.time = []
		self.pathlength = []
		self.nodeexpanded = []

		self.astar()
		self.uniformcost()
		self.weightedAStarManhattan1()
		self.weightedAStarManhattan2()
		self.weightedAStarEuclidean1()
		self.weightedAStarEuclidean2()
		self.weightedAStarDiagonal1()
		self.weightedAStarDiagonal2()
		self.weightedAStarChebyshev1()
		self.weightedAStarChebyshev2()

		self.writeToExcel("Tests/Trials1.xls")


	def astar(self):
		for i in range(10):
			with AStar(self.grid.cells, self.grid.startLocations[i], self.grid.goalLocations[i]) as astar:
				self.grid.resetAlgoCells()
				found = astar.search()
				if(found):
					self.grid.setPath(astar.getPath())
					self.time.append(astar.time)
					self.pathlength.append(astar.pathlength)
					self.nodeexpanded.append(astar.nodeexpanded)


	def uniformcost(self):
		for i in range(10):
			with UniformCost(self.grid.cells, self.grid.startLocations[i], self.grid.goalLocations[i]) as uniformCost:
				self.grid.resetAlgoCells()
				found = uniformCost.search()
				if(found):
					self.grid.setPath(uniformCost.getPath())
					self.time.append(uniformCost.time)
					self.pathlength.append(uniformCost.pathlength)
					self.nodeexpanded.append(uniformCost.nodeexpanded)


	def weightedAStarManhattan1(self):
		for i in range(10):
			with WeightedAStar(self.grid.cells, self.grid.startLocations[i], self.grid.goalLocations[i], Test.ManhattanDistance, 1.25) as weightedAStar:
				self.grid.resetAlgoCells()
				found = weightedAStar.search()
				if(found):
					self.grid.setPath(weightedAStar.getPath())
					self.time.append(weightedAStar.time)
					self.pathlength.append(weightedAStar.pathlength)
					self.nodeexpanded.append(weightedAStar.nodeexpanded)


	def weightedAStarManhattan2(self):
		for i in range(10):
			with WeightedAStar(self.grid.cells, self.grid.startLocations[i], self.grid.goalLocations[i], Test.ManhattanDistance, 2) as weightedAStar:
				self.grid.resetAlgoCells()
				found = weightedAStar.search()
				if(found):
					self.grid.setPath(weightedAStar.getPath())
					self.time.append(weightedAStar.time)
					self.pathlength.append(weightedAStar.pathlength)
					self.nodeexpanded.append(weightedAStar.nodeexpanded)


	def weightedAStarEuclidean1(self):
		for i in range(10):
			with WeightedAStar(self.grid.cells, self.grid.startLocations[i], self.grid.goalLocations[i], Test.EuclideanDistance, 1.25) as weightedAStar:
				self.grid.resetAlgoCells()
				found = weightedAStar.search()
				if(found):
					self.grid.setPath(weightedAStar.getPath())
					self.time.append(weightedAStar.time)
					self.pathlength.append(weightedAStar.pathlength)
					self.nodeexpanded.append(weightedAStar.nodeexpanded)


	def weightedAStarEuclidean2(self):
		for i in range(10):
			with WeightedAStar(self.grid.cells, self.grid.startLocations[i], self.grid.goalLocations[i], Test.EuclideanDistance, 2) as weightedAStar:
				self.grid.resetAlgoCells()
				found = weightedAStar.search()
				if(found):
					self.grid.setPath(weightedAStar.getPath())
					self.time.append(weightedAStar.time)
					self.pathlength.append(weightedAStar.pathlength)
					self.nodeexpanded.append(weightedAStar.nodeexpanded)


	def weightedAStarChebyshev1(self):
		for i in range(10):
			with WeightedAStar(self.grid.cells, self.grid.startLocations[i], self.grid.goalLocations[i], Test.ChebyshevDistance, 1.25) as weightedAStar:
				self.grid.resetAlgoCells()
				found = weightedAStar.search()
				if(found):
					self.grid.setPath(weightedAStar.getPath())
					self.time.append(weightedAStar.time)
					self.pathlength.append(weightedAStar.pathlength)
					self.nodeexpanded.append(weightedAStar.nodeexpanded)


	def weightedAStarChebyshev2(self):
		for i in range(10):
			with WeightedAStar(self.grid.cells, self.grid.startLocations[i], self.grid.goalLocations[i], Test.ChebyshevDistance, 2) as weightedAStar:
				self.grid.resetAlgoCells()
				found = weightedAStar.search()
				if(found):
					self.grid.setPath(weightedAStar.getPath())
					self.time.append(weightedAStar.time)
					self.pathlength.append(weightedAStar.pathlength)
					self.nodeexpanded.append(weightedAStar.nodeexpanded)


	def weightedAStarDiagonal1(self):
		for i in range(10):
			with WeightedAStar(self.grid.cells, self.grid.startLocations[i], self.grid.goalLocations[i], Test.DiagonalDistance, 1.25) as weightedAStar:
				self.grid.resetAlgoCells()
				found = weightedAStar.search()
				if(found):
					self.grid.setPath(weightedAStar.getPath())
					self.time.append(weightedAStar.time)
					self.pathlength.append(weightedAStar.pathlength)
					self.nodeexpanded.append(weightedAStar.nodeexpanded)


	def weightedAStarDiagonal2(self):
		for i in range(10):
			with WeightedAStar(self.grid.cells, self.grid.startLocations[i], self.grid.goalLocations[i], Test.DiagonalDistance, 2) as weightedAStar:
				self.grid.resetAlgoCells()
				found = weightedAStar.search()
				if(found):
					self.grid.setPath(weightedAStar.getPath())
					self.time.append(weightedAStar.time)
					self.pathlength.append(weightedAStar.pathlength)
					self.nodeexpanded.append(weightedAStar.nodeexpanded)


	# Write to excel sheet
	def writeToExcel(self, filename):
		book = xlwt.Workbook()
		sheet = book.add_sheet("Map")

		sheet.write(1, 0, "Start")
		sheet.write(1, 1, "Goal")

		sheet.write(13, 0, "Average")

		sheet.write(0, 3, "AStar")
		sheet.write(1, 3, "Time")
		sheet.write(1, 4, "Path Length")
		sheet.write(1, 5, "Nodes Expanded")

		sheet.write(0, 7, "Uniform Cost")
		sheet.write(1, 7, "Time")
		sheet.write(1, 8, "Path Length")
		sheet.write(1, 9, "Nodes Expanded")

		sheet.write(0, 11, "Manhattan 1.25")
		sheet.write(1, 11, "Time")
		sheet.write(1, 12, "Path Length")
		sheet.write(1, 13, "Nodes Expanded")

		sheet.write(0, 15, "Manhattan 2")
		sheet.write(1, 15, "Time")
		sheet.write(1, 16, "Path Length")
		sheet.write(1, 17, "Nodes Expanded")

		sheet.write(0, 19, "Euclidean 1.25")
		sheet.write(1, 19, "Time")
		sheet.write(1, 20, "Path Length")
		sheet.write(1, 21, "Nodes Expanded")

		sheet.write(0, 23, "Euclidean 2")
		sheet.write(1, 23, "Time")
		sheet.write(1, 24, "Path Length")
		sheet.write(1, 25, "Nodes Expanded")

		sheet.write(0, 27, "Diagonal 1.25")
		sheet.write(1, 27, "Time")
		sheet.write(1, 28, "Path Length")
		sheet.write(1, 29, "Nodes Expanded")

		sheet.write(0, 31, "Diagonal 2")
		sheet.write(1, 31, "Time")
		sheet.write(1, 32, "Path Length")
		sheet.write(1, 33, "Nodes Expanded")

		sheet.write(0, 35, "Chebyshev 1.25")
		sheet.write(1, 35, "Time")
		sheet.write(1, 36, "Path Length")
		sheet.write(1, 37, "Nodes Expanded")

		sheet.write(0, 39, "Chebyshev 2")
		sheet.write(1, 39, "Time")
		sheet.write(1, 40, "Path Length")
		sheet.write(1, 41, "Nodes Expanded")


		# Write start/goal locations
		for i in range(0, 10):
			sheet.write(i+2, 0, "".join(["(", str(self.grid.startLocations[i].X), ",", str(self.grid.startLocations[i].Y), ")"]))
			sheet.write(i+2, 1, "".join(["(", str(self.grid.goalLocations[i].X), ",", str(self.grid.goalLocations[i].Y), ")"]))

		# Astar
		for i in range(0, 10):
			sheet.write(i+2, 3, float(self.time[i]))
			sheet.write(i+2, 4, float(self.pathlength[i]))
			sheet.write(i+2, 5, float(self.nodeexpanded[i]))
		sheet.write(13, 3, sum(self.time[0:10]) / 10)
		sheet.write(13, 4, sum(self.pathlength[0:10]) / 10)
		sheet.write(13, 5, sum(self.nodeexpanded[0:10]) / 10)

		# Uniform
		for i in range(10, 20):
			sheet.write(i-8, 7, float(self.time[i]))
			sheet.write(i-8, 8, float(self.pathlength[i]))
			sheet.write(i-8, 9, float(self.nodeexpanded[i]))
		sheet.write(13, 7, sum(self.time[10:20]) / 10)
		sheet.write(13, 8, sum(self.pathlength[10:20]) / 10)
		sheet.write(13, 9, sum(self.nodeexpanded[10:20]) / 10)


		# Manhattan 1.25
		for i in range(20, 30):
			sheet.write(i-18, 11, float(self.time[i]))
			sheet.write(i-18, 12, float(self.pathlength[i]))
			sheet.write(i-18, 13, float(self.nodeexpanded[i]))
		sheet.write(13, 11, sum(self.time[20:30]) / 10)
		sheet.write(13, 12, sum(self.pathlength[20:30]) / 10)
		sheet.write(13, 13, sum(self.nodeexpanded[20:30]) / 10)

		# Manhattan 2
		for i in range(30, 40):
			sheet.write(i-28, 15, float(self.time[i]))
			sheet.write(i-28, 16, float(self.pathlength[i]))
			sheet.write(i-28, 17, float(self.nodeexpanded[i]))
		sheet.write(13, 15, sum(self.time[30:40]) / 10)
		sheet.write(13, 16, sum(self.pathlength[30:40]) / 10)
		sheet.write(13, 17, sum(self.nodeexpanded[30:40]) / 10)

		# Euclidean 1.25
		for i in range(40, 50):
			sheet.write(i-38, 19, float(self.time[i]))
			sheet.write(i-38, 20, float(self.pathlength[i]))
			sheet.write(i-38, 21, float(self.nodeexpanded[i]))
		sheet.write(13, 19, sum(self.time[40:50]) / 10)
		sheet.write(13, 20, sum(self.pathlength[40:50]) / 10)
		sheet.write(13, 21, sum(self.nodeexpanded[40:50]) / 10)

		# Euclidean 2
		for i in range(50, 60):
			sheet.write(i-48, 23, float(self.time[i]))
			sheet.write(i-48, 24, float(self.pathlength[i]))
			sheet.write(i-48, 25, float(self.nodeexpanded[i]))
		sheet.write(13, 23, sum(self.time[50:60]) / 10)
		sheet.write(13, 24, sum(self.pathlength[50:60]) / 10)
		sheet.write(13, 25, sum(self.nodeexpanded[50:60]) / 10)

		# Diagonal 1.25
		for i in range(60, 70):
			sheet.write(i-58, 27, float(self.time[i]))
			sheet.write(i-58, 28, float(self.pathlength[i]))
			sheet.write(i-58, 29, float(self.nodeexpanded[i]))
		sheet.write(13, 27, sum(self.time[60:70]) / 10)
		sheet.write(13, 28, sum(self.pathlength[60:70]) / 10)
		sheet.write(13, 29, sum(self.nodeexpanded[60:70]) / 10)

		# Diagonal 2
		for i in range(70, 80):
			sheet.write(i-68, 31, float(self.time[i]))
			sheet.write(i-68, 32, float(self.pathlength[i]))
			sheet.write(i-68, 33, float(self.nodeexpanded[i]))
		sheet.write(13, 31, sum(self.time[70:80]) / 10)
		sheet.write(13, 32, sum(self.pathlength[70:80]) / 10)
		sheet.write(13, 33, sum(self.nodeexpanded[70:80]) / 10)

		# Chebyshev 1.25
		for i in range(80, 90):
			sheet.write(i-78, 35, float(self.time[i]))
			sheet.write(i-78, 36, float(self.pathlength[i]))
			sheet.write(i-78, 37, float(self.nodeexpanded[i]))
		sheet.write(13, 35, sum(self.time[80:90]) / 10)
		sheet.write(13, 36, sum(self.pathlength[80:90]) / 10)
		sheet.write(13, 37, sum(self.nodeexpanded[80:90]) / 10)

		# Chebyshev 2
		for i in range(90, 100):
			sheet.write(i-88, 39, float(self.time[i]))
			sheet.write(i-88, 40, float(self.pathlength[i]))
			sheet.write(i-88, 41, float(self.nodeexpanded[i]))
		sheet.write(13, 39, sum(self.time[90:100]) / 10)
		sheet.write(13, 40, sum(self.pathlength[90:100]) / 10)
		sheet.write(13, 41, sum(self.nodeexpanded[90:100]) / 10)


		# Save excel sheet
		book.save(filename)


	# Optimized for the vertical and horizontal path
	def ManhattanDistance(s, goal):
		dx = abs(s.X - goal.X)
		dy = abs(s.Y - goal.Y)

		return 0.25 * (dx + dy)

	# Straight line distance
	def EuclideanDistance(s, goal):
		dx = abs(s.X - goal.X)
		dy = abs(s.Y - goal.Y)

		return 0.25 * math.sqrt(dx*dx + dy*dy)

	# Max of values
	def ChebyshevDistance(s, goal):
		dx = abs(s.X - goal.X)
		dy = abs(s.Y - goal.Y)

		return max(dx, dy)

	# PRefer diagonal
	def DiagonalDistance(s, goal):
		d_max = max(abs(s.X - goal.X), abs(s.Y - goal.Y))
		d_min = min(abs(s.Y - goal.Y), abs(s.Y - goal.Y))

		horizontal_min = 0.25
		diagonal_min = 1.41421356237
		
		return diagonal_min * d_min + horizontal_min * (d_max - d_min)



# Check if this script is being run directly (if it is, then __name__ becomes __main__)
if __name__ == '__main__':
	test = Test()

