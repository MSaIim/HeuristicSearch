import xlwt, sys
import Utilities.Constants
import Algorithms.Formulas as Formulas
import Tests.ExcelLists as ExcelLists
from Grid.Grid import Grid
from Algorithms.AStar import AStar
from Algorithms.WeightedAStar import WeightedAStar
from Algorithms.UniformCost import UniformCost


class MapTester(object):
	def __init__(self, mapList, excelSheet):
		self.grid = Grid()
		self.book = xlwt.Workbook()
		self.sheet = self.book.add_sheet("Benchmarks")

		# Save info
		self.mapList = mapList
		self.excelSheet = excelSheet

		# Lists to keep the data
		self.time = []
		self.pathlength = []
		self.nodeexpanded = []


	# Open the map and run the algorithms
	def run(self):
		index = 0

		for map in self.mapList:
			print("> ", end="")
			sys.stdout.flush()

			# Load map and run algorithms
			self.grid.load(map)
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

			# Write to Excel sheet
			self.writeToExcel(index)

			# Clear lists for next map
			self.time.clear()
			self.pathlength.clear()
			self.nodeexpanded.clear()

			# Map done
			index += 1
			print(''.join(["[Map", str(index), " DONE]"]))

		# Save excel sheet
		self.book.save(self.excelSheet)


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

		print(".", end="")
		sys.stdout.flush()


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

		print(".", end="")
		sys.stdout.flush()


	def weightedAStarManhattan1(self):
		for i in range(10):
			with WeightedAStar(self.grid.cells, self.grid.startLocations[i], self.grid.goalLocations[i], Formulas.ManhattanDistance, 1.25) as weightedAStar:
				self.grid.resetAlgoCells()
				found = weightedAStar.search()
				if(found):
					self.grid.setPath(weightedAStar.getPath())
					self.time.append(weightedAStar.time)
					self.pathlength.append(weightedAStar.pathlength)
					self.nodeexpanded.append(weightedAStar.nodeexpanded)

		print(".", end="")
		sys.stdout.flush()


	def weightedAStarManhattan2(self):
		for i in range(10):
			with WeightedAStar(self.grid.cells, self.grid.startLocations[i], self.grid.goalLocations[i], Formulas.ManhattanDistance, 2) as weightedAStar:
				self.grid.resetAlgoCells()
				found = weightedAStar.search()
				if(found):
					self.grid.setPath(weightedAStar.getPath())
					self.time.append(weightedAStar.time)
					self.pathlength.append(weightedAStar.pathlength)
					self.nodeexpanded.append(weightedAStar.nodeexpanded)

		print(".", end="")
		sys.stdout.flush()


	def weightedAStarEuclidean1(self):
		for i in range(10):
			with WeightedAStar(self.grid.cells, self.grid.startLocations[i], self.grid.goalLocations[i], Formulas.EuclideanDistance, 1.25) as weightedAStar:
				self.grid.resetAlgoCells()
				found = weightedAStar.search()
				if(found):
					self.grid.setPath(weightedAStar.getPath())
					self.time.append(weightedAStar.time)
					self.pathlength.append(weightedAStar.pathlength)
					self.nodeexpanded.append(weightedAStar.nodeexpanded)

		print(".", end="")
		sys.stdout.flush()


	def weightedAStarEuclidean2(self):
		for i in range(10):
			with WeightedAStar(self.grid.cells, self.grid.startLocations[i], self.grid.goalLocations[i], Formulas.EuclideanDistance, 2) as weightedAStar:
				self.grid.resetAlgoCells()
				found = weightedAStar.search()
				if(found):
					self.grid.setPath(weightedAStar.getPath())
					self.time.append(weightedAStar.time)
					self.pathlength.append(weightedAStar.pathlength)
					self.nodeexpanded.append(weightedAStar.nodeexpanded)

		print(".", end="")
		sys.stdout.flush()


	def weightedAStarChebyshev1(self):
		for i in range(10):
			with WeightedAStar(self.grid.cells, self.grid.startLocations[i], self.grid.goalLocations[i], Formulas.ChebyshevDistance, 1.25) as weightedAStar:
				self.grid.resetAlgoCells()
				found = weightedAStar.search()
				if(found):
					self.grid.setPath(weightedAStar.getPath())
					self.time.append(weightedAStar.time)
					self.pathlength.append(weightedAStar.pathlength)
					self.nodeexpanded.append(weightedAStar.nodeexpanded)

		print(".", end="")
		sys.stdout.flush()


	def weightedAStarChebyshev2(self):
		for i in range(10):
			with WeightedAStar(self.grid.cells, self.grid.startLocations[i], self.grid.goalLocations[i], Formulas.ChebyshevDistance, 2) as weightedAStar:
				self.grid.resetAlgoCells()
				found = weightedAStar.search()
				if(found):
					self.grid.setPath(weightedAStar.getPath())
					self.time.append(weightedAStar.time)
					self.pathlength.append(weightedAStar.pathlength)
					self.nodeexpanded.append(weightedAStar.nodeexpanded)

		print(".", end="")
		sys.stdout.flush()


	def weightedAStarDiagonal1(self):
		for i in range(10):
			with WeightedAStar(self.grid.cells, self.grid.startLocations[i], self.grid.goalLocations[i], Formulas.DiagonalDistance, 1.25) as weightedAStar:
				self.grid.resetAlgoCells()
				found = weightedAStar.search()
				if(found):
					self.grid.setPath(weightedAStar.getPath())
					self.time.append(weightedAStar.time)
					self.pathlength.append(weightedAStar.pathlength)
					self.nodeexpanded.append(weightedAStar.nodeexpanded)

		print(".", end="")
		sys.stdout.flush()


	def weightedAStarDiagonal2(self):
		for i in range(10):
			with WeightedAStar(self.grid.cells, self.grid.startLocations[i], self.grid.goalLocations[i], Formulas.DiagonalDistance, 2) as weightedAStar:
				self.grid.resetAlgoCells()
				found = weightedAStar.search()
				if(found):
					self.grid.setPath(weightedAStar.getPath())
					self.time.append(weightedAStar.time)
					self.pathlength.append(weightedAStar.pathlength)
					self.nodeexpanded.append(weightedAStar.nodeexpanded)

		print(".", end="")
		sys.stdout.flush()


	# Write to excel sheet
	def writeToExcel(self, row):
		# Print the map number above start write_merge(top_row, bottom_row, left_column, right_column)
		map_cell = xlwt.easyxf('pattern: pattern solid, fore_colour light_blue;' 'font: colour white, bold True;')
		self.sheet.write_merge(ExcelLists.dataRows[row]-2, ExcelLists.dataRows[row]-2, 0, 1, ''.join(["Map", str(row+1)]), map_cell)

		# Print the headers
		algo_cell = xlwt.easyxf('pattern: pattern solid, fore_colour black;' 'font: colour white, bold True;')
		for i in range(len(ExcelLists.headers)):
			if(ExcelLists.headers[i][1] == 0):
				self.sheet.write_merge(ExcelLists.dataRows[row]-2, ExcelLists.dataRows[row]-2, ExcelLists.headers[i][2], ExcelLists.headers[i][2]+2, ExcelLists.headers[i][0], algo_cell)
			elif(ExcelLists.headers[i][1] == 1):
				self.sheet.write(ExcelLists.dataRows[row]-1, ExcelLists.headers[i][2], ExcelLists.headers[i][0])
			else:
				self.sheet.write(ExcelLists.avgHeader[row][1], ExcelLists.avgHeader[row][2], ExcelLists.avgHeader[row][0])

		# Write start/goal locations
		for i in range(0, 10):
			self.sheet.write(ExcelLists.dataRows[row]+i, 0, "".join(["(", str(self.grid.startLocations[i].X), ",", str(self.grid.startLocations[i].Y), ")"]))
			self.sheet.write(ExcelLists.dataRows[row]+i, 1, "".join(["(", str(self.grid.goalLocations[i].X), ",", str(self.grid.goalLocations[i].Y), ")"]))

		# Get the data from the algorithms
		for col in range(len(ExcelLists.dataCols)):
			for i in range(10):
				self.sheet.write(ExcelLists.dataRows[row]+i, ExcelLists.dataCols[col], self.time[i])
				self.sheet.write(ExcelLists.dataRows[row]+i, ExcelLists.dataCols[col]+1, self.pathlength[i])
				self.sheet.write(ExcelLists.dataRows[row]+i, ExcelLists.dataCols[col]+2, self.nodeexpanded[i])

			# Get average of column
			self.sheet.write(ExcelLists.dataRows[row]+11, ExcelLists.dataCols[col], sum(self.time[ExcelLists.dataAvgs[col][0]:ExcelLists.dataAvgs[col][1]]) / 10)
			self.sheet.write(ExcelLists.dataRows[row]+11, ExcelLists.dataCols[col]+1, sum(self.pathlength[ExcelLists.dataAvgs[col][0]:ExcelLists.dataAvgs[col][1]]) / 10)
			self.sheet.write(ExcelLists.dataRows[row]+11, ExcelLists.dataCols[col]+2, sum(self.nodeexpanded[ExcelLists.dataAvgs[col][0]:ExcelLists.dataAvgs[col][1]]) / 10)

